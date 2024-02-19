# PyCryption 
 

# 🔐 CryptoWallet to Encrypt Files

###### tags: `Bloom Week1`



# :mag: How does it work?

## :camera: UML diagrams
### Shan wants to send a `message` to Shiva

![image](https://user-images.githubusercontent.com/30176438/132206323-072bfead-e86c-4acc-8803-b8ee904c33e8.png)


## :book: Detailed Explaination

1. Shan requests for Shiva's `public_key`
2. Shan performs `symmetric encryption` on the `message`
3. Shan encrypts the `symmetric_key` using Shiva's public key
4. Shan signs the `encrypted_message` using Shan's `private_key`
5. Shan sends the `public_key` of Shan, `encrypted_message`, `encrypted_symmetric_key` and `signature` to Shiva
6. Shiva verifies the `encrypted_message` using the signature and Shan's `public_key`
7. Shiva decryptes the `encrypted_symmetric_key` using Shiva's `private_key`
8. Shiva decryptes the `encrypted_message` using `symmetric_key`


## :rocket: Features

- [x] Symmetric Encryption
- [x] Asymmetric Encryption
- [x] Signing messages
- [x] Verifying signature
- [x] Dockerized the application

## 🖭 How does each file work?

### :rocket: [create_keys.py](https://github.com/ShivaShanmuganathan/PyCryption/blob/master/create_keys.py)

- Using RSA to generate Public and Private key of  Receiver

```
import rsa

#----------CREATING RECEIVER'S PUBLIC & PRIVATE KEYS------------#

# CREATE THE PUB & PRIVATE KEYS
(pubkey,privkey)=rsa.newkeys(2048)

# WRITE THE PUBLIC KEY TO A FILE
pukey = open('publickey.key','wb')
pukey.write(pubkey.save_pkcs1('PEM'))
pukey.close()

# WRITE THE PRIVATE KEY TO A FILE
prkey = open('privkey.key','wb')
prkey.write(privkey.save_pkcs1('PEM'))
prkey.close()

print('PUBLIC & PRIVATE KEY OF RECEIVER HAS BEEN GENERATED')

```



---


### :rocket: [encrypt.py](https://github.com/ShivaShanmuganathan/PyCryption/blob/master/encrypt.py)
### Shan performs encryption and signs the message
- Perform `Symmetric Encryption` on the `Message`
- Encrypt `Symmetric_Key` using Shiva's `Public_Key`
- Generate `public_key` and `private_key` for Shan
- Sign the `encrypted_message` using Shan's `private_key`

### These 4 Files need to be sent to Shiva

##### 1. `encrypted_symmetric_key` 
##### 2. Shan's `public_key`
##### 3. `signature` 
##### 4. `encrypted_message`


``` 
from cryptography.fernet import Fernet
import rsa

#----------FILE ENCRYPTION USING SYMMETRIC KEY---------------#
# CREATE THE SYMMETRIC KEY AND CIPHER
symKey = Fernet.generate_key()
cipher = Fernet(symKey)

# GET FILENAME TO ENCRYPT
filename = input("Enter filename to encrypt [with extension]:\n")
myfile = open(filename,'rb')
myfiledata = myfile.read()

# ENCRYPT THE DATA AND CREATE ENCRYTPED FILE
encrypted_data = cipher.encrypt(myfiledata)
edata = open('enc_' + filename ,'wb')
edata.write(encrypted_data)


#----------USING RECEIVER'S PUBLIC KEY TO ENCRYPT SYMMETRIC KEY------------#
# OPEN AND LOAD THE PUBLIC KEY FILE OF RECEIVER
pkey = open('publickey.key','rb')
pkdata = pkey.read()
pubkey = rsa.PublicKey.load_pkcs1(pkdata)

# ENCRYPT THE SYMMETRIC KEY WITH THE PUBLIC KEY
encrypted_key = rsa.encrypt(symKey,pubkey)
ekey = open('encrypted_key','wb')
ekey.write(encrypted_key)


#----------USING SENDER'S PRIVATE KEY TO SIGN MESSAGE------------#
# GENERATE ASYMMETRIC KEY PAIR [to use for signature]
(public_key, private_key) = rsa.newkeys(512)
vkey = open('public_verify.key','wb')
vkey.write(public_key.save_pkcs1('PEM'))
vkey.close()

# GENERATE SIGNATURE FILE
signature = rsa.sign(encrypted_data, private_key, 'SHA-1')
sign = open('sign.txt','wb')
sign.write(signature)
sign.close()


print('------- ENCRYPTION COMPLETE ---------')
print('\n')
print(' YOU CAN NOW SHARE THE ENCRYPTED FILE: _enc' +filename+ '\n' );
print(' YOU CAN NOW SHARE THE ENCRYPTED SYMMETRIC KEY: encrypted_key \n' );
print(' YOU CAN NOW SHARE THE PUBLIC KEY OF SENDER: public_verify.key \n' );
print(' YOU CAN NOW SHARE THE SIGNATURE: sign.txt \n' );
```



---


### :rocket: [decrypt.py](https://github.com/ShivaShanmuganathan/PyCryption/blob/master/decrypt.py)
### Shiva performs decryption and verifies the message
- Shiva's `private_key` is used to decrypt the `encrypted_symmetric_key`
- `symmetric_key` is used to decrypt the `Message`
- `signature` is verified using Shan's `public_key`

### Shiva can now access the decrypted message.



``` 
import rsa
from cryptography.fernet import Fernet


# OEPN RECEIVER'S PRIVATE KEY [to decrypt the symmetric key]
prkey = open('privkey.key','rb')
pkey = prkey.read()
private_key = rsa.PrivateKey.load_pkcs1(pkey)

# DECRYPT SYMMETRIC KEY USING RECEIVER'S PRIVATE KEY
s = open('encrypted_key','rb')
sym = s.read()
symKey = rsa.decrypt(sym,private_key)
cipher = Fernet(symKey)

# DECRYPTION USING CIPHER OF SYMMETRIC KEY
filename = input("Enter filename to decrypt [with extension]:\n")
encrypted_data = open(filename,'rb')
edata = encrypted_data.read()
decrypted_data = cipher.decrypt(edata)
message = decrypted_data


# OPENING THE PUBLIC KEY OF SENDER AND SIGNATURE
vkey = open('public_verify.key','rb')
vdata = vkey.read()
public_verify = rsa.PublicKey.load_pkcs1(vdata)
sign = open('sign.txt','rb')
signature = sign.read()


# VERIFYING SIGNATURE
try:
    rsa.verify(edata, signature, public_verify)
    print('signature verified')
    # load the file
    with open('decrypted_' + filename,'wb') as df:
        df.write(decrypted_data)
    print('Check----->'+ 'decrypted_'+filename+ '<------to get the decrypted file')

except:
    print('message is tampered')
 ```

---------------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------------------


## Dockerized Python Encryptor - How do I run this?


1. Encrypt your file. 
2. Transfer the encrypted file.
3. It can be decrypted only by the intended receiver.



### PLEASE NOTE 
#### You can use `raze.png` OR `document.txt` for Encryption 
#### If you wish to use your own files for encryption, you need to move them to repository's directory, and add the below line to Dockerfile 
#### `COPY filename.ext .`

---------------------------------------------------------------------------------------------------------------------------------------------------------------------


---------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Step 1: Build The Docker Image

  ```sh
  docker build -t pycryptor .
  ```



---------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Step 2: Start The Docker Container

### PLEASE NOTE
#### Before running the below docker command, make sure to replace '/my/dir' with the path of the directory where you want to have the Keys & Encrypted/Decrypted files
  ```sh
  docker run -d --name pycryption -v /my/dir:/usr/src/app -ti pycryptor
  ```
### Example 
  ```sh
  docker run -d --name pycryption -v /home/playground/Bloom/pycryptor:/usr/src/app -ti pycryptor
  ```

---------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Step 3 [RECEIVER]: Creating Public And Private Keys For Receiver

  ```sh
  docker exec -it pycryption python create_keys.py
  ```

### *** RECEIVER'S PUBLIC KEY IS SHARED TO THE SENDER ***
#### Only `publickey.key` is shared
#### `privatekey.key` is not shared 

---------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Step 4 [SENDER]: Sender Encrypts & Signs The File

#### 1. Perform Symmetric Encryption on the file you choose
#### 2. Symmetric Key is encrypted using Receiver's Public Key
#### 3. Create Public & Private Keys for Sender
#### 4. Encrypted data is signed using Sender's Private Key

  ```sh
  docker exec -it pycryption python encrypt.py
  ```
#### When Prompted, Enter name of document to be encrypted [with extension] 
#### Example: `raze.png` OR `document.txt`  `[filename.ext]`

### *** 4 FILES ARE SHARED TO RECEIVER ***
#### *** ENCRYPTED FILE ***  `enc_raze.png` OR `enc_document.txt` `[enc_filename.ext]`
#### *** ENCRYPTED SYMMTERIC KEY *** `encrypted_key`
#### *** SENDER'S PUBLIC KEY *** `public_verify.key`
#### *** SIGNATURE *** `sign.txt`

---------------------------------------------------------------------------------------------------------------------------------------------------------------------


## Step 5 [RECEIVER]: Receiver Decrypts File & Verifies The Signature

#### 1. Encrypted data is verified using Sender's Public Key
#### 2. Encrypted Symmetric Key is decrypted using Receiver's Private Key
#### 3. Decrypting the encrypted file using symmetric key

  ```sh
  docker exec -it pycryption python decrypt.py
  ```

#### When Prompted, Enter name of document to be decrypted [with extension] 
#### Example: `enc_raze.png` OR `enc_document.txt` `[enc_filename.ext]`

## You can check the decrypted files 
#### Example: `decrypted_enc_raze.png` OR `decrypted_enc_document.txt` `[decrypted_enc_filename.ext]`

---------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Step 6 [RECEIVER/SENDER]: Stop The Container 
  ```sh
  docker stop pycryption
  ```


---------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Step 7 [RECEIVER/SENDER]: Remove The Container & Image
### Remove the Container
  ```sh
  docker rm pycryption
  ```

### Remove the Image
  ```sh
  docker rmi pycryptor
  ```
