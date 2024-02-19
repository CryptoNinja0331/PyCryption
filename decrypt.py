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