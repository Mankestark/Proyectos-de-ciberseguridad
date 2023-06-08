# Iron Dome, monitorización.
Monitoriza carpetas, ficheros y ficheros por extensión. Se
ejecuta como servicio en segundo plano, con permisos de
administrador. Informa si hay actividad criptográfica, 
de posibles '_ransomware_', cambios en la entropía e
integridad de los ficheros monitorizados. Advierte del
uso excesivo del disco (tasa de E/S) y consumo excesivo de
CPU. En caso de que la aplicación exceda de 100Mb de uso
de la memoria física termina, evita una sobrecarga del
sistema provocada por sí mismo.
## Contenedores.
El directorio por defecto a monitorizar es '_/data_',
este puede montarse como volumen sobre un directorio
existente del equipo anfritión.
Para indicar otro directorio/s o fichero/s distinto 
a '_/data_' se realiza cargando la variable de
entorno '_DIRMON_' con la carpeta a monitorizar 
al ejecutar '_docker_'. Este mismo procedimiento 
se aplica para indicar las extensiones, 
incluyendolas dentro de la variable de entorno '_EXTMON_'.
Estas pueden cargarse dentro del fichero '.env', sin 
tener que especificarlas dentro del '_Dockerfile_' o
'_Dockercompose.yaml_'.
## Comprobaciones
Probar tasa consumo de disco con:
iostat -d -k -p /dev/<disco>