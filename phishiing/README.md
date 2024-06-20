# Proyecto de Seguridad Informática

Este repositorio contiene el desarrollo de ejercicios prácticos para la asignatura de Seguridad Informática, basados en el uso de Kali Linux y la herramienta `setoolkit` para realizar ataques de ingeniería social. A continuación se detalla el contenido del proyecto.

## Ejercicio 1: Instalación de Kali Linux en VirtualBox

### Paso 1: Configuración de la Máquina Virtual

1. **Nombre y Carpeta**: Nombramos la máquina virtual como "Kali" y seleccionamos la carpeta de destino y la ISO de Kali Linux.
2. **Procesadores y Memoria RAM**: Configuramos la máquina con tres procesadores y la cantidad de memoria RAM deseada.

### Paso 2: Instalación de Kali Linux

1. **Adaptador de Red**: Seleccionamos el adaptador de red en modo NAT para asignar una IP oculta.
2. **Instalación Gráfica**: Iniciamos la instalación gráfica y seleccionamos los idiomas y distribuciones de teclado.
3. **Nombre de Usuario y Contraseña**: Asignamos el nombre de la máquina y creamos el usuario con su contraseña.
4. **Particionado de Disco**: Elegimos el particionado guiado, seleccionamos el disco y optamos por instalar el GRUB.

## Ejercicio 3: Ataque de Ingeniería Social con `setoolkit`

### Paso 3.1: Clonación de URL para Obtener Credenciales

1. **Inicio de `setoolkit`**: Abrimos una terminal e iniciamos `setoolkit` en modo superusuario, aceptando los términos y condiciones.
2. **Selección de Opciones**:
   - Opción 2: Ataques web.
   - Opción 3: Ataques de credenciales.
   - Opción 2: Clonación de URL de credenciales.
3. **Configuración de Clonación**:
   - Introducimos la IP de la máquina (por defecto) y la URL a clonar.
4. **Introducción de Credenciales**: Ingresamos las credenciales en la web clonada y verificamos la captura de credenciales.

### Paso 3.2: Envío de Correo de Phishing

1. **Selección de Opciones en `setoolkit`**:
   - Opción 1: Ingeniería social.
   - Opción 5: Envío masivo de emails.
2. **Configuración del Correo**:
   - Selección de envío a una sola dirección.
   - Redacción del email en texto plano, engañando a la víctima para que pulse el enlace de la web clonada.
3. **Envío del Correo**:
   - Ingresamos el email del destinatario y seleccionamos enviar desde una cuenta de Gmail.
   - Configuramos el asunto y la contraseña del email.
   - Optamos por no agregar malware y enviamos el email.
4. **Verificación**: Comprobamos que el email ha llegado al destinatario con el contenido correcto.

---

Este README proporciona una guía paso a paso para realizar las tareas descritas en el proyecto, permitiendo replicar el entorno y los ataques de ingeniería social documentados. Para cualquier consulta adicional, por favor contacte al autor del proyecto.
