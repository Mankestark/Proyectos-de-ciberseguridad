# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scorpion.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mariza <mariza@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/23 13:33:15 by mariza            #+#    #+#              #
#    Updated: 2023/04/24 13:33:12 by mariza           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import os 
from datetime import datetime
import argparse
from PIL import Image
from PIL.ExifTags import TAGS
import requests
def exifdatos (img):
    try:
        imagen = os.stat(img)
        print(f'Fecha de creacion  \t: {datetime.fromtimestamp(imagen.st_ctime)}')
        print(f'Fecha de modificacion \t: {datetime.fromtimestamp(imagen.st_mtime)}')
    except:
        sys.exit('Imagen invalida')
            
    try:
        image = Image.open(img)
        exifdata = image.getexif()
        if len(exifdata) == 0:
            sys.exit('La imagen no tiene metadatos')
        else:
            info = {}
            for x, y in exifdata.items():
                tagname = TAGS.get(x, x)
                info[tagname] = y
                    
            for x, y in info.items():
                print(f'{x:25}: {y}')
    except:
        print('Imagen no tiene datos EXIF')

if __name__ == "__main__":

    if len(sys.argv) > 1:
       exifdatos(sys.argv[1])
    else:
        print('Introduzca una imagen por favor. ')
 
