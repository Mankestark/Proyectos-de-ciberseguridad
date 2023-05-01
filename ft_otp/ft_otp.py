# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_otp.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mankestarkdev <mankestarkdev@student.42    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/24 14:03:36 by mariza            #+#    #+#              #
#    Updated: 2023/04/24 22:40:41 by mankestarkd      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


import argparse
import time


parser = argparse.ArgumentParser()
parser.add_argument('-g', help = 'Clave en hexadecimal')
parser.add_argument('-k', help = 'Generacion de nueva clave temporal')
args = parser.parse.args()

    
if __name__ == "__main__":