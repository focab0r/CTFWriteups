# Rusia #

- **Tipo:** Estego
- **Autor:** Bara
- **Autor del Writeup:** [focab0r](https://github.com/focab0r)
- **Flag:** `HackOn{la_muñeca_de_la_muñeca_de_la_muñeca_de_la_muñeca}`

### Descripcion ###

Quería ir a Rusia para traerte algo de recuerdo, pero por culpa de la guerra me cancelaron el vuelo.

Te dejo esta foto que he encontrado por ahí para que te acuerdes de mi.

## WriteUp ##

Al descargar la imagen, ya nos podemos fijar que la imagen pesa mas de lo normal. Esto significa, por lo tanto, que contiene archivos ocultos en el interior. Se pueden extraer mediante "binwalk":
```
binwalk -e image.jpg
```
Con esto, nos aparecen 5 imagenes, de las que a su vez se pueden sacar otras 5 imagenes. Se trata de una muñeca rusa. Si analizamos el sistema de las imagenes, podemos construir un script como el siguiente que vaya recorriendo todas las ramas de la muñeca y calculando el hash de las hojas del arbol.

Una vez que encontremos una con un hash diferente, podremos suponer que es la flag.
```
#!/bin/bash

binwalk -e image.jpg
cd _image.jpg.extracted

rm *zip
binwalk -e *
rm *jpg
for i in 3 4 5
do
	dira=_${i}.jpg.extracted
	cd $dira
	for e in $(seq 5)
	do
		arch=${e}.jpg
		binwalk -e $arch > /dev/null
		diraNEW=_${e}.jpg.extracted
		cd $diraNEW
		for a in $(seq 5)
		do
			archNEW=${a}.jpg
			binwalk -e $archNEW > /dev/null
			echo -e "\n INFOOOOO i = $i, e = $e, a = $a\n"
			LASTPATH=_${a}.jpg.extracted
			cd $LASTPATH
			binwalk -e 5.jpg > /dev/null
			cd _5.jpg.extracted
			binwalk -e 4.jpg > /dev/null
			cd _4.jpg.extracted
			binwalk -e 3.jpg > /dev/null
			cd _3.jpg.extracted
			binwalk -e 2.jpg > /dev/null
			cd _2.jpg.extracted
			value=$(md5sum 1.jpg | awk '{print $1}' FS=' ')
			echo -e "THE VALUE IS: $value"
			cd ..
			cd ..
			cd ..
			cd ..
			cd ..
		done
		rm *zip
		cd ..
	done
	rm *zip 
	cd ..
done
```
Tras esperar unos segundos, vemos un hash que difiere con el de todas las demas imagenes:
```
 INFOOOOO i = 3, e = 5, a = 1

THE VALUE IS: 7942ebec9f84449cbcf7473c39390d73

 INFOOOOO i = 3, e = 5, a = 2

THE VALUE IS: 7942ebec9f84449cbcf7473c39390d73

 INFOOOOO i = 3, e = 5, a = 3

THE VALUE IS: 7942ebec9f84449cbcf7473c39390d73

 INFOOOOO i = 3, e = 5, a = 4

THE VALUE IS: d9edbed71896a207b210d5c154bef686
```
Yendo a `_3.jpg.extracted`, luego a `_5.jpg.extracted` y por ultimo a `_4.jpg.extracted`, llegamos finalmente a la imagen `1.jpg`. Si extraemos los archivos que contiene mediante binwalk, obtenemos `flag.txt`, donde esta la flag.
