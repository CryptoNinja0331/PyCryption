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
