# Guuglu #

- **Tipo:** Web
- **Autor del Writeup:** [focab0r](https://github.com/focab0r)
- **Flag:** `?`

### Descripcion ###


## WriteUp ##

Leyendo el codigo fuente, se ve que la flag se encuentra en un post del admin, solo visible por el.

En los archivos del bot, el `docker-compose.yml` contiene la contraseña de prueba del admin: `PASSWD=tDGfsG8btQzHdIklM5I4`. Probandola en la pagina web del reto, funciona, y nos logueamos como admin obteniendo asi la flag. 

F.
