# rev01 #

- **Tipo:** Reversing 
- **Autor:** Deloitte
- **Autor del Writeup:** [dtorresss](https://github.com/dtorresss)
- **Flag:** `flag{4LW4YS_3NCRYPT_F1RMW4RES}`

## WriteUp ##

Al descomprimir el zip del reto nos encontamos con un archivo llamado "firmware.bin". Podemos intentar hacer un strings del archivo pero será imposible llegar a ver nada.
Si usamos la herramienta binwalk podemos ver que detecta varios "Zip archive data". Entonces probamos haciendo `unzip firmware.bin` y efectivamente lo podemos descomprimir.

Ahora nos aparece una carpeta llamada "sistema ficheros". Si volvemos a ver el binwalk anterior podemos ver que hay varias rutas interesantes. Una de ella es `root/PARA LOS DEVELOPERS.txt`. Este archivo al hacerle un `cat` nos dice: 

```
Os habeis olvidado quitar el software "keypass" que revela la contraseña por defecto de todos nuestros routers.
Porfavor quitarlo en el siguiente update

Gracias! El CISO
```
Esto es interesante ya que hay otra ruta llamada `challenge/`. Si hacemos un file al archivo keepass que hay en él vemos que se trata de un "Java archive data (JAR)". Entonces para ejecutarlo podemos hacer `java -jar keepass` y tendríamos la flag.

