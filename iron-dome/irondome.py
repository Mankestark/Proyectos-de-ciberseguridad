#!/usr/bin/env python3
import sys
import time
import multiprocessing as mp
import os
import argparse
import pathlib
import psutil
import signal
from math import log2
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
from ironaux import check_disk_activity, crypt_activity, \
    init_log, is_root, check_malware_ext



MAXDISKACTIVITY = 200  # Max. actividad en disco en KB/seg.

MONEXTENSION = ''

class Irondome(FileSystemEventHandler):
    def __init__(self, pathtomonit):
        self.path = pathtomonit
        self.last_entropy = self.entropy_sum()

    # calcula la entropia de archivo o directorio
    def entropy_sum(self):
        extensions = MONEXTENSION
        if not os.path.exists(self.path):
            return -1.0
        if os.path.isfile(self.path):
            try:
                with open(self.path, 'rb') as f:
                    data = f.read()
            except Exception as err:
                print(f'Se ha producido un error {err} en {self.path}')
        elif os.path.isdir(self.path):
            data = b""
            for root, dirs, files in os.walk(self.path):
                for file in files:
                    
                    file_path = os.path.join(root, file)
                    if extensions:
                        ext = pathlib.Path(file_path)
                        if not any([extension in ext.suffix for extension in extensions]):
                            continue
                    try:
                        with open(file_path, 'rb') as f:
                            data += f.read()
                    except Exception as err:
                        logging.critical(f'Se ha producido un error {err} en {self.path}')
                        print(f'Se ha producido un error {err} en {self.path}')
        else:
            return -1.0
        frequency = [0] * 256
        for character in data:
            frequency[character] += 1
        entropy = 0
        data_length = len(data)
        for count in frequency:
            if count == 0:
                continue
            probability = count / data_length
            entropy += probability * log2(probability)
        logging.debug(f'Calculada entropia: {self.path} = {entropy}')
        return entropy

    def test_file(self, event):
        
        if os.path.isfile(event.src_path):
            retchkm = check_malware_ext(event.src_path)
            if retchkm == 'OK':
                return
            if retchkm == 'RANSOM':
                logging.critical(f'Actividad RANSOMWARE en: {event.src_path}')
                return
            if retchkm == 'INVALID':
                logging.critical(f'Fichero Altamente sospechoso: {event.src_path}. '
                                 f'Posible actividad malware.')
                return
            if retchkm == 'UNCERTAIN':
                logging.warning(f'Fichero desconocido: {event.src_path}. '
                                f'Posible actividad '
                                f'malware/criptografica. Revise fichero.')
                return
            logging.warning(f'Error al obtener el tipo de fichero de: {event.src_path}')

    def on_created(self, event):
        self.test_file(event)

    def on_modified(self, event):
        self.test_file(event)
        file_entropy = self.entropy_sum()
        if file_entropy != self.last_entropy:
            
            logging.warning(f'Hay cambios en la entropia {event.src_path}')
            logging.debug(f'    Entropia anterior: {abs(self.last_entropy)}')
            logging.debug(f'    Entropia actual: {abs(file_entropy)}')
        self.last_entropy = file_entropy


class Checker:
    def __init__(self, path):
        self.observer = Observer()
        self.path = path

    def run(self):
        def all_signals_handler(signum, frame):
            print(f"Se ha recibido la señal ({signum}). Cerrando")
            logging.warning(f"Se ha recibido la señal ({signum}). Cerrando")
            self.observer.stop()
            time.sleep(1)
            exit(0)

        for sig in [signal.SIGINT, signal.SIGTERM, signal.SIGQUIT, signal.SIGHUP]:
            signal.signal(sig, all_signals_handler)

        event = Irondome(self.path)
        self.observer.schedule(event, self.path, recursive=True)
        self.observer.start()
        try:
            while True:
                check_disk()
                check_criptography()
                memory_usage()
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            print('Stoped')
        self.observer.join()


def check_disk():
    
    disk_rate = check_disk_activity()
    if disk_rate > 80:
        logging.warning(f'Abuso en disco detectado: {disk_rate:.2f} KB/s')


def check_criptography():
    mem = psutil.virtual_memory()
    total = mem.percent
    cpu_percent = psutil.cpu_percent(interval=0.1)
    if cpu_percent and total > MAXDISKACTIVITY:
        logging.critical('Hay abuso de CPU, posible actividad criptografica', cpu_percent)
    proc_nom, proc_pid = crypt_activity()
    if proc_pid:
        logging.critical(f'ATENCION: Actividad criptografica/ransomware en: \'{proc_nom}\' pid={proc_pid}')


def memory_usage():
    pid = psutil.Process(os.getpid())
    mem = pid.memory_info().rss // 1048576
    if mem > 100:
        logging.critical('Ha sobrepasado el limite de memoria')
        exit()


def proceso(path):
    Checker(path).run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, nargs='+', help='define uno o varios directorios o archivos')
    parser.add_argument('-e', type=str, nargs='+', help='escanea solo las extensiones introducidas')
    args = parser.parse_args()
    paths = args.path
    # MONEXTENSION=args.e
    # if not MONEXTENSION:
    #     MONEXTENSION=os.getenv('EXTMON')
    print(f'DEBUG0 args.e: {args.e}, type: {type(args.e)}')
    print(f'DEBUG0 EXTMON: {os.getenv("EXTMON")}, type: {os.getenv("EXTMON")}')
    MONEXTENSION = args.e if args.e else os.getenv('EXTMON')
    print(f'DEBUG MONEXTENSION: {MONEXTENSION}, type: {type(MONEXTENSION)}')
    if type(MONEXTENSION) == str:
        MONEXTENSION = MONEXTENSION.split()
    print(f'DEBUG1 MONEXTENSION: {MONEXTENSION}, type: {type(MONEXTENSION)}')

    DIRMON = os.getenv('DIRMON')
    if len(paths) == 1 and paths[0] == '/data':
        if DIRMON:
            print(f'DIRMON={DIRMON}, paths={paths}')
            paths = DIRMON.split()
            print(f'DDIRMON={DIRMON}, paths={paths}')
        print(f'DDDIRMON={DIRMON}, paths={paths}')
    print(f'4DIRMON={DIRMON}, paths={paths}')

    procs = []
    init_log()
    print('Iniciando.')
    if not is_root():
        logging.critical('User is not root')
        print('El usuario debe de ser root.')
        exit(3)
    logging.info('''Se aconseja monitorizar los directorios:
    - /etc
    - /root ''')
    for path in paths:
        
        print(f'DEBUG0 EXTMON: {os.getenv("EXTMON")}, type: {os.getenv("EXTMON")}')
        if not os.path.exists(path):
            print(f'No existe: {path}', file=sys.stderr)
            logging.critical(f'No existe: {path}')
            continue
        proc = mp.Process(target=proceso, args=(path,))
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()
