# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mariza <mariza@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/20 12:14:52 by mariza            #+#    #+#              #
#    Updated: 2023/04/25 11:26:12 by mariza           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from bs4 import BeautifulSoup
import requests
import os.path
import argparse
from urllib.parse import urlparse, urljoin
import os
import sys


parser = argparse.ArgumentParser()
parser.add_argument ('-r', action="store_true",  help = 'forma recursiva')
parser.add_argument ('-l', type = int, default = 5, help = 'numero de profundidad')
parser.add_argument ('-p', type = str, default = 'data', help = 'ruta hacia la carpeta defaut: data')
parser.add_argument ('url', type = str, help = 'url para buscar')
args = parser.parse_args()
def get_images_local(url, folder, recursive=False, numlinks=0, l=5):
    
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    try:             
        l = 0
        with open(urlparse(url).netloc) as url:
            text = url.read()
        
        soup = BeautifulSoup(text, 'html.parser')
        
        images = soup.find_all('img')
        
        if not images:
            print(f'No hay imagenes que descargar')
            return
            
        for x in images:
            url_imagenes = x['src']
            ext = url_imagenes.split('.')[-1].lower()
            extensions = ['jpg', 'png', 'gif', 'jpeg', 'bmp']
            if ext in extensions:
                image_name = url_imagenes.split('/')[-1]
                image_folder = f"{folder}/{image_name}"
                try:
                    with open(image_folder, 'wb') as handler:
                        imagen = requests.get(url_imagenes).content
                        handler.write(imagen)
                        print(f"Descargada la imagen {image_name}")
                except:
                    print('Imagen invalida')
    except requests.exceptions.RequestException:
        print('Url invalid')   

def get_images(url, folder, recursive=False, numlinks=0, l=5):
    
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    try:     
        r = requests.get(url)
            
            
        soup = BeautifulSoup(r.content, 'html.parser')
        
        images = soup.find_all('img')
        
        if not images:
            print(f'No hay imagenes que descargar en el level{numlinks}')
            return
            
        for x in images:
            url_imagenes = x['src']
            ext = url_imagenes.split('.')[-1].lower()
            
            if urlparse(url_imagenes).scheme != urlparse(url).scheme:
                url_imagenes = urljoin(url, url_imagenes)
            
            extensions = ['jpg', 'png', 'gif', 'jpeg', 'bmp']
            
            if ext in extensions:
                image_name = url_imagenes.split('/')[-1]
                image_folder = f"{folder}/{image_name}"
                
                with open(image_folder, 'wb') as handler:
                    imagen = requests.get(url_imagenes).content
                    handler.write(imagen)
                    print(f"Descargada la imagen {image_name}")           
        
        if recursive and numlinks < l:
            url_links = soup.find_all('a')
            
            if not url_links:
                print('No hay links')
                return
            
            for links in url_links:
                href = links.get('href')
                if href and href.startswith('http'):
                    if urlparse(href).netloc == urlparse(url).netloc:
                        subfolder = f"{folder}/{numlinks+1}"
                        get_images(href, subfolder, numlinks+1, l)
    except requests.exceptions.RequestException:
        print('Url invalid')
        
 
if __name__ == "__main__":
      
    num_link = 0
    if urlparse(args.url).scheme == 'file':
        get_images_local(args.url, args.p, args.r, num_link, args.l)
    else:
        get_images(args.url, args.p, args.r, num_link, args.l)
           