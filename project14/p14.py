import hashlib
from Cryptodome.Cipher import AES

from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from gmssl import sm2
import time
PK= '77A8C798B2DC25D6E9819713976D38A52D45AA623C87BA294955A2AE498CEFDCC6E32B66C067BAE6B04D8CD638B3FC1C37F6563C6B38D0077EE17C666F308933'
RK = '52D45AA623C87BA294955A2AE498CEFDCC6E32B66C077A8C798B2DC25D6E9819713976D38A52D45AA623C8767878545C37F6563C6B38D0077EE17C666F308933'

def sm2_enc(session_key):#sm2加密会话密钥
    sm2_crypt = sm2.CryptSM2(public_key=PK, private_key=RK)
    return sm2_crypt.encrypt(session_key)
def AES_enc(hash_data,session_key):
    iv = get_random_bytes(16)#初始值
    cipher = AES.new(session_key, AES.MODE_CBC, iv)#确定AES加密的模式和iv，用会话密钥作为密钥
    return cipher.encrypt(pad(hash_data, AES.block_size))#填充为128bit的倍数
def PGP(data):

    #会话密钥
    session_key = get_random_bytes(16)
    
    #aes加密消息
    #压缩消息
    hash_data = hashlib.sha256(data).digest()+data#H(M)||M
  
    #aes对称加密
    ciphertext_aes =AES_enc(hash_data,session_key)

    #sm2加密会话密钥
    ciphertext_sm2 = sm2_enc(session_key)

    #拼合并转为文本数据
    ciphertext=(ciphertext_sm2+ciphertext_aes).hex().encode('utf-8')#sm2(sk)||AES(H(M)||M)

    return ciphertext

data=b'data'
start=time.time()
for i in range(10000):
    pgp_data=PGP(data)
end=time.time()
print("PGP加密结果:\n",pgp_data,"\n")
print("加密一次所用时间:\n",(end-start)/10000,"s")

