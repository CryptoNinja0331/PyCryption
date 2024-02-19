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