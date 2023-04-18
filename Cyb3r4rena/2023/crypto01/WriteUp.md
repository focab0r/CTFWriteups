# crypto01 # 

- **Tipo:** Criptografía
- **Autor:** Deloitte
- **Autor del Writeup:** [dtorresss](https://github.com/dtorresss)
- **Flag:** `flag{Crypt0_$3cur3d}`

## Writeup ##

Al descomprimir el zip del reto, nos encontramos con un .txt y otro .zip. Si intentamos descomprimir el zip nos pedirá una contraseña. Si leemos el archivo nos daremos cuenta de que parece un texto con algún tipo de rotación. Si lo metemos en [Cyberchef](https://cyberchef.org) descubrimos que era un simple ROT13 con la siguiente información:

```
Bienvenidos,

Este es el primer mensaje secreto.
Una simple rotacion trece, el resto no serán tan sencillos...
Utiliza la siguiente contraseña para descomprimir el ZIP

flag:{z1p_P4$$w0rd!}
```
Tenemos entonces ahora la contraseña del zip.
Lo descomprimimos y aparecerán otros dos archivos, Clave.txt e Instrucciones.txt.
El archivo Instrucciones nos dice:

```

Ahora que nos hemos asegurado de que no nos lee cualquiera, te dare alguna indicación extra, aunque necesitamos tomar más precauciones antes por si acaso alguien consigue leer este mensaje...

Mensaje RC4:

5B 26 FC 85 E4 F8 6A 86 FE 9A E5 DD 25 30 71 09 5C 2B AA 66 96 86 95 3B F5 4A 8B B5 8D 5C 06 B2 48 2A 36 1D B0 10 F0 40 01 E0 31 7F DC CE E4 B9 33 A3 0C 7D CD D4 5F 13 5A F0 63 28 53 F9 4C 23 0E BB 76 66 FF 9B 78 3E C4 E4 98 E8 31 60 9A BA 01 F7 94 59 CD 81 3F 2E DC 3B 51 ED
```

Y en la Clave tenemos:

```
KzxWZTY/WEkvST9YSS9JP1hJL0k/WEkvST9YSS9JP1hJL0k/WEkvST9YSS9JP1hJL0k/WEkvST9YSS9JP1hJL0k/T0BudUhwJ1ZVNFp0cWs0WnRxazRadHFrNFp0cWs0WnRxazRadHFrNFp0cWs0WnRxazRadHFrNFp0cWs0WnRxazRadHJVJDZVST0rQ0FJdStDQUpfP1hJL0k/WEkvSSs8WSN1P1hJL0k/WEkvST9RXkk2KzxWZEwrPFZkTCtGXGNnSVhXRCY0V28rWis8WiY5P1lVXSs5T0NAdThSRyVyOFJIM1QrQT8tNj9WK1RyP1YrVT4rPFZkTCs8VmRMKzxWZExJWFpgcElOVWQ6K0ZGTT0rRklPJz9YSS9JP1hJL0k/WEkvST9YSS9JP1hJL0k/WEkvST9YSS9JP1hGcF8/WEkvST9YRnBfP1hJL0k/VGdQWkhqVXU9SHM5cmI4UkclcjhSRyVyOFJHJXI4UkclcjhSRyVyOFJHJXI4Ukclcj5wKj9ZP1YrVTM+cCo/WThSRyVyOFJHYk4kNlVJPT5AMWBFOFJHJXI4UkclcjhSRyVyOFJHJXI4UkclcjhSRyVyPnAoODsrPFZkTD9RXkk2K0JyMkU/VitUcj9YOCRkKzxaJjk/WEhCMzhSRyVyOFJHJXI4UkclcjhSRyVyOFJHJXI4UkcudT9YSjEnK0NBPls/IWVdcz5AMHMvOFJHJXI/JGx1JStGSUMjP1hJL0k4UkclcjhSRyVyOFJHJXI4UkclcjhSRyVyOFJHaDM/WDRkWT9WK1RyP1g0ZFk/VitUcj9XOC5xSGpVdT1IbHVYIz9WK1UzOFJHaDM/WEkvST9YSS9JP1hJL0k/WEhCMz9WRmc0K0NBSl8/WEkvST9RYFFbP1hIQjM4Ukg0WyQ2VUk9K0RZUDYzWnFtP0YoSTxnKzxWZEwrPFZkTCs8VmRMKzxWZEwrPFZkTCs8VmRMKzxWZEwrPFZkTCs8VmRMKzxaJT0rPFomPT9YSS9JP1hJL0k/WEkvST9YSS9JP1hJL0k/WEkvST9YSS9JP1hJL0k/WEkvST9YSS9JP1hJL0k/WEkvST9bTQ==
```

Vamos a usar cyberchef de nuevo.
Pasamos la clave por él e imnediatamente nos detecta que esta encodeado en base64 y base85 mostrandonos la clave: base85

```
   __________________________________________________
  |==================================================|
  | __  ___________  ___________            ~~~~~ == |
  |[_j  L_I_I_I_I_j  L_I_I_I_I_j            ~~~~~ == |
  |________________________________ _______ ______==_|
  |[__I_I_I_I_I_I_I_I_I_I_I_I_I_I_] [__I__] [_I_I_I_]|
  |[___I_I_I_I_I_I_I_I_I_I_I_I_]  |    _    [_I_I_I_]|
  |[__I_I_I_I_I_I_I_I_I_I_I_I_L___|  _[_]_  [_I_I_I_]|
  |[_____I_I_I_I_I_I_I_I_I_I_I____] [_I_I_] [_I_I_T ||
  | [__I__I_________________I__L_] ________ [___I_I_j|
  | key: base85                                      |
  |__________________________________________________|
```

Entonces como indica en las instrucciones en cyberchef ahora buscamos el bloque RC4 y ponemos la contraseña "base85" indicando que el input está en hexadecimal.
Y de esta manera conseguiremos la flag:

```

Felicidades, has demostrado ser valido para conocer el secreto final:

flag:{Crypt0_$3cur3d}
```
