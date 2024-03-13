# Crypto tree #

- **Tipo:** Cripto
- **Autor del Writeup:** [focab0r](https://github.com/focab0r)
- **Flag:** `HackOn{827cfbe07f8ffde1c7b457d148075082}`

### Descripcion ###

My uncle sent me his Instagram password by email because he suspects that it was leaked in some very popular dictionary with passwords from several years ago, the problem is that we lost the part of the message where the password was, luckily I asked him to send me the root of the Merkle tree to check that the message had not been altered along the way. Do you think that with this you can find out his password?

Message: The password that I use is the same as in the Google account it is ????
Root Merkle tree: 30c085686aa4b1d76ac1c72dfefab6f4a02f5e3865acd76f868b6d5781d2efc8

Once you get the password, the flag is HackOn{\<hash md5 of the password\>}
