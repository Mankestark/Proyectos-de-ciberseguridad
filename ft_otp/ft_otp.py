#!/goinfre/mariza/miniconda3/envs/42AI-mariza/bin/python

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_otp.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mariza <mariza@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/24 14:03:36 by mariza            #+#    #+#              #
#    Updated: 2023/04/28 10:07:25 by mariza           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


import argparse, time, hashlib, os, hmac, base64, struct
from base64 import b64encode, b64decode, b32encode


parser = argparse.ArgumentParser()
parser.add_argument('-g', type = str, default = 'key.hex', help = 'Clave en hexadecimal')
parser.add_argument('-k', help = 'Generacion de nueva clave temporal')
args = parser.parse_args()

def generador_clave(text):
    h = hashlib.sha256(b'text')
    clave = (h.hexdigest())
    with open('key.hex', 'w+') as f:
        f.write(clave)
    
def  generador_key(file_key):
    with open(file_key, 'r') as f:
        clave  = f.read()
    encode = clave.encode('utf-8')
    clave32 = b32encode(encode)
    with open('ft_otp.key', 'w+') as f:
        f.write(clave32.decode())
            
def generador_hotp(key, intervals_no):
    clave = base64.b32decode(key, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(clave, msg, hashlib.sha1).digest()
    o = o = h[19] & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return h
    
def generador_totp(key):
    x =str(generador_hotp(key,intervals_no=int(time.time())//30))
    while len(x)!=6:
        x+='0'
    return x
    
if __name__ == "__main__":
    
    path = 'key.hex'
    try:
        if os.path.exists(path):
            generador_key(args.g)
        else:
            text = input('El archivo .hex no existe introduzca una clave ')
            generador_clave(text)
            generador_key('key.hex')
            print('La clave ha sido guardada en ft_otp.key')
    except:
        print('El archivo introducido no es valido introduzca key.hex')
    if args.k:
        try:
            with open(args.k, 'r') as f:
                key = f.read()
            print(generador_totp(key))
        except:
            print('Tiene que ingresar ft_otp.key')

        
    
  
    
          
 
