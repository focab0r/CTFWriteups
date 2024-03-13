# Crypto tree #

- **Tipo:** Cripto
- **Autor del Writeup:** [focab0r](https://github.com/focab0r)
- **Flag:** `HackOn{827cfbe07f8ffde1c7b457d148075082}`

### Descripcion ###

My uncle sent me his Instagram password by email because he suspects that it was leaked in some very popular dictionary with passwords from several years ago, the problem is that we lost the part of the message where the password was, luckily I asked him to send me the root of the Merkle tree to check that the message had not been altered along the way. Do you think that with this you can find out his password?

Message: The password that I use is the same as in the Google account it is ????
Root Merkle tree: 30c085686aa4b1d76ac1c72dfefab6f4a02f5e3865acd76f868b6d5781d2efc8 

Once you get the password, the flag is HackOn{\<hash md5 of the password\>}

## Writeup ##

Un arbol de Merkle es una estructura en la que se realiza el hash de un objeto, sumandolo despues a otro hash, y volviendo a realizar el hash. En pocas palabras, algo así.

```
OBJETO_1	OBJETO_2	OBJETO_3	OBJETO_4
   |		   |		   |		   |
 Hash_1		 Hash_2		 Hash_3		 Hash_4
   |---------------|		   |---------------|
	   |				   |
	   |				   |
    Hash_1 + Hash_2		    Hash_3 + Hash_4
	   |				   |
         Hash_5				 Hash_6
	   |-------------------------------|
			   |
			   |
		    Hash_5 + Hash_6
			   |
		       Hash_Raiz
```

Lo que hay que hay que hacer por tanto es bruteforcear el objeto 4 y realizar el arbol de Merkle, para despues comparar con el del enunciado y ver si coinciden.

La principal dificultad en este reto consistia en saber si los objetos eran las letras o las palabras. Para probar ambos metodos, se contruye un script como el de la solucion, utilizando como diccionario el `rockyou.txt` (habla de un diccionario muy popular). Tratando a las palabras como objetos, se obtiene la contraseña.
```
Password: thereisnopassword
MD5: 827cfbe07f8ffde1c7b457d148075082
```
