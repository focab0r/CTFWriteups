# stego01 #

- **Tipo:** Estego
- **Autor:** Deloitte
- **Autor del Writeup:** [focab0r](https://github.com/focab0r)
- **Flag:** `flag{R4ns0mw4r3_R \-/|_|k}`

## WriteUp ##

La herramienta "stegseek" permite hacer un ataque de fuerza bruta para intentar hallar una clave valida con la que extraer archivos de la imagen:
```
stegseek moscowland.jpg /usr/share/wordlists/rockyou.txt
```
Lanzandola se obtiene la clave "conti", y se extrae una dll a "moscowland.jpg.out". Haciendo un strings al archivo, obtenemos la flag.
```
strings moscowland.jpg.out
```
