FROM debian:latest

#paquetes de instalacion
RUN set -x &&  apt-get update -y
RUN  yes | apt install nginx  
RUN	 yes | apt-get install tor  
RUN	 yes | apt-get install openssh-server 
RUN yes | apt-get install sudo 

#archivos de configuracion
COPY index.html /var/www/html/index.html
COPY torrc /etc/tor/torrc
COPY sshd_config /etc/ssh/sshd_config

#configuracion ssh
RUN useradd -m manuel \
	&& echo "manuel:onion" | chpasswd

EXPOSE 80
EXPOSE 4242
 
