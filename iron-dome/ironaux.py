#!/usr/bin/env python3
import os.path
import time
import logging
from os import path, getuid
from math import log2
from psutil import Process, process_iter, disk_io_counters
from mimetypes import guess_type
from magic import from_file

RANSOMEXT = ('.ft', '.locky', '.crypt', '.xtbl', '.zepto', '.cerber',
             '.cerber3', 'onion', '.thor', '.aaa', '.xyz', '.zzz', '.micro',
             '.mira', '.locked')

CRYPTOCMDS = ('gpg', '-encrypt', 'encrypt', 'crypt', '.crypt', 'stockholm',
              'ft_stockholm', 'AES', 'DES', 'RSA', 'MD5', 'miner',
              'ethereum', 'monero', 'bitcoin', 'cryptonight')

FILELOGIRON: str = '/var/log/irondome.log'


def fentropy(file_path: str) -> float:
    data: bytes
    frequency: list
    count: int
    character: int
    probability: float
    entropy: float

    if not path.isfile(file_path):
        return -1.0
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
    except Exception:
        logging.error('Error al abrir el fichero', exc_info=True)
        return -2.0
    return entropia(data)
    # Count the frequency of each byte
    # frequency = [0] * 256
    # for character in data:
    #     frequency[character] += 1
    # # Calculate entropy
    # entropy = 0
    # for count in frequency:
    #     if count == 0:
    #         continue
    #     probability = count / len(data)
    #     entropy -= probability * log2(probability)
    # return entropy


# Minima entropia 0 (cadena vacia)
def entropia(data):
    if not len(data):
        return 0.0
    frequency = [0] * 256
    for character in data:
        frequency[character] += 1
    # Calculate entropy
    entropy = 0
    for count in frequency:
        if count == 0:
            continue
        probability = count / len(data)
        entropy -= probability * log2(probability)
    return entropy


def get_memory_main() -> float:
    # Obtiene la memoria del proceso actual en bytes
    proceso: Process
    memory_usage: int
    memory_usage = Process().memory_info().rss

    # convierte los bytes a Mb y retorna
    return float(memory_usage / (1024 ** 2))


def is_root() -> bool:
    return getuid() == 0


def crypt_activity(cmdscrypto: list = CRYPTOCMDS):
    namecrypt: str = ''
    pidcrypt: int = 0
    proclist: list
    command: str
    _rcmd: list

    if type(cmdscrypto) != list and type(cmdscrypto) != tuple:
        return namecrypt, -1

    proclist = process_iter(['cmdline', 'name', 'pid'])
    for _proc in proclist:
        _rcmd = _proc.info['cmdline']
        if not _rcmd:
            continue
        command = " ".join(_rcmd)
        if any(cmd in command for cmd in cmdscrypto):
            namecrypt = _proc.info['name']
            pidcrypt = _proc.info['pid']
            break

    return namecrypt, pidcrypt


def get_ext(nom: str) -> str:
    _, ext = path.splitext(nom)
    return ext

def magic_file_type(nomfile: str) -> str:
    """
Check if file type of is right with its extension
    :param nomfile:
    :return: None is file not found
             ERROR is file extesion not eq to file ext.
             UNKNOWN file unknown for mimetypes and magic (very suspect file)
             NOMIME file unknown for mimetype (suspect file)
             NOMAGIC file unknown for magc (suspenct file)
             file is OK
    """
    magicfile: str
    mimefile: str
    if not path.isfile(nomfile):
        return None
    try:
        magicfile = from_file(nomfile, mime=True)
    except FileNotFoundError:
        return None
    mimefile = guess_type(nomfile)[0]
    # print(f'mimefile: {magicfile} - guess_type: {guess_type(nomfile)[0]}, {guess_type(nomfile)[1]}')
    if not all([magicfile, mimefile]):
        return 'UNKNOWN'
    if not magicfile:
        return 'NOMAGIC'
    if not mimefile:
        return 'NOMIME'
    if magicfile != mimefile:
        return 'ERROR'
    return magicfile

# Comprueba si es una extension, no sospechosa de ransomware
# Retorna: OK si es valida.
#          RANSOM si es sospecho, extension ransom
#          INVALID ext. no se corresponde con tipo fichero
#          UNCERTAIN sospechoso, incierto
#          ERROR no existe el fichero
def check_malware_ext(nom: str) -> str:
    retcall: str
    if any([rext in get_ext(nom) for rext in RANSOMEXT]):
        return 'RANSOM'
    retcall = magic_file_type(nom)
    if not retcall:
        return 'ERROR'
    if retcall == 'ERROR':
        return 'INVALID'
    if retcall == 'UNKNOWN' or \
            retcall == 'NOMIME' or \
            retcall == 'NOMAGIC':
        return 'UNCERTAIN'
    return 'OK'


# Definir la tasa máxima de entrada/salida permitida y el tiempo de la última llamada
MAX_IO_RATE = 1000  # KB/s
ult_llamada_time = time.time()
io_counters_ini = disk_io_counters()


# Función para monitorear la tasa de entrada/salida de disco
def check_disk_activity() -> float:
    global ult_llamada_time  # utilizar la variable global
    global io_counters_ini  # variable global io anterior
    tiempo_transcur: float  # Tiempo transcurrido desde la última llamada
    io_rate: float
    io_counters: object

    # Obtener los tiempos totales de entrada/salida desde el inicio del sistema
    io_counters = disk_io_counters()
    if io_counters == io_counters_ini:
        return 0.0

    # Calcular el tiempo transcurrido desde la última llamada
    tiempo_transcur = time.time() - ult_llamada_time
    ult_llamada_time = time.time()

    # Calcular la tasa de entrada/salida en KB/s utilizando el tiempo transcurrido
    io_rate = (io_counters.read_bytes - io_counters_ini.read_bytes
               + io_counters.write_bytes -
               io_counters_ini.write_bytes) / (1024 * tiempo_transcur)
    # print(f'ioread={io_counters.read_bytes}, ioreadini={io_counters_ini.read_bytes}\n'
    #       f'io_rate={io_rate}')
    if io_rate:
        io_counters_ini = io_counters
    # Comprobar si la tasa es demasiado alta
    # if io_rate > MAX_IO_RATE:
    #     print(f"Se ha producido un incremento en la "
    #           f"entrada/salida del disco de {io_rate:.2f} KB/s. "
    #           f"Puede que haya un abuso de disco en el sistema.")
    # Retorna la entrada/salida total lecturas+escrituras en KB/s
    return io_rate


def init_log(logname: str = FILELOGIRON) -> str:
    try:
        logging.basicConfig(filename=logname, level=logging.INFO, # filemode='w',
                            format='%(asctime)s %(levelname)s: %(message)s',
                            datefmt='%b %d %X')
    except PermissionError:
        logname = f'/tmp/{path.basename(logname)}'
        if not init_log(logname):
            print(f'Error to open {logname}')
            return ''
    logging.info(f'Logging Init on: {logname}')
    return logname


if __name__ == '__main__':

    def count_elapsed_time(f):
        """
        Decorator.
        Execute the function and calculate the elapsed time.
        Print the result to the standard output.
        """

        def wrapper(*args, **kwargs):
            # Start counting.
            start_time = time.time()
            # Take the original function's return value.
            ret = f(*args, **kwargs)
            # Calculate the elapsed time.
            elapsed_time = time.time() - start_time
            print("Elapsed time: %0.10f seconds." % elapsed_time)
            return ret

        return wrapper


    @count_elapsed_time
    def time_fentropy(filename):
        return fentropy(filename)

    print('Guardando logs en: ', init_log())
    logging.info('Testing...')
    logging.info(f'Calculo entropia /etc/profile: {time_fentropy("/etc/profile")}')
    logging.info(f'Memoria usada: {get_memory_main():.2f} Mb')
    logging.info(f'{get_ext("/tmp/p.ext")}')

    proc: int
    nameproc: str

    nameproc, proc = crypt_activity(['bash'])
    if proc:
        print(f'Actividad crypto/malware detectada en {nameproc}, pid={proc}')

    if not check_disk_activity():
        print('Esperando 5 seg. para calcular tasa IO')
        time.sleep(5)
    print(f'Tasa de consumo de disco: {check_disk_activity():.2f} KB/s')

    print(check_malware_ext('/tmp/test/a.png'))
    print(check_malware_ext('/tmp/test/a.ft'))
    print(check_malware_ext('/tmp/test/a.qwerty'))
    print(check_malware_ext('/tmp/test/a.txt'))
    print(check_malware_ext('/tmp/test/a'))