import socket
from os.path import commonprefix
import random

from gmssl import sm3
from gmpy2 import invert
import sys
# Addition on elliptic curves (x,y)=(x1,y1)+(x2,y2)
def add_ECC(x1,y1,x2,y2):
    if x1 == x2 and y1 == p-y2:
        return False
    if x1!=x2:
        r=((y2 - y1) * invert(x2 - x1, p))%p
    else:
        r=(((3 * x1 * x1 + a)%p) * invert(2 * y1, p))%p
        
    x = (r * - x1 - x2)%p
    y = (r * (x1 - x) - y1)%p
    return x,y

# The dot product on an elliptic curve k*(x,y)
def mul_ECC(xtmp,ytmp,ktmp):
    ktmp = ktmp%p
    ktmp = bin(ktmp)[2:]
    rx,ry = xtmp,ytmp
    for i in range(1,len(ktmp)):
        rx,ry = add_ECC(rx, ry, rx, ry)
        if ktmp[i] == '1':
            rx,ry = add_ECC(rx, ry, xtmp, ytmp)
    return rx%p,ry%p
# Elliptic curve parameter
p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3    
a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
X = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
Y = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2

# Calculate the SM3 hash
def sm3_hash(msg):
    msg=msg.encode()
    msg=bytearray(msg)
    h = sm3.sm3_hash(msg)
    return h
#建立连接
alice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
alice_addr = ('localhost', 50007)
alice.bind(alice_addr)

alice.listen(1)
print('connecting...')

bob, addr = alice.accept()
print('Bob has connected!')


d1=random.randint(1,n-1)

#p1=d1^(-1)·G
p1=mul_ECC(X,Y,invert(d1,p))
x,y=hex(p1[0]),hex(p1[1])

#  p1

bob.sendto(x.encode(),addr)
bob.sendto(y.encode(),addr)

# Set z to be identifier for both parties, message is m
m="message"
z="_bob"
e=sm3_hash(m+z)


k1=random.randint(1,n-1)

# q1=k1·G
q1=mul_ECC(X,Y,k1)
x,y=hex(q1[0]),hex(q1[1])

# q1,e
bob.sendto(x.encode(),addr)
bob.sendto(y.encode(),addr)
bob.sendto(e.encode(),addr)

# 接受 r,s2,s3
r,addr=bob.recvfrom(1024)
r=int(r.decode(),16)

s2,addr=bob.recvfrom(1024)
s2=int(s2.decode(),16)

s3,addr=bob.recvfrom(1024)
s3=int(s3.decode(),16)
print("r:",r)
print("s2:",s2)
print("s3:",s3)
# (生成签名 s=(d1*k1)*s2+d1*s3-r mod n
s=((d1*k1)*s2+d1*s3-r)%n

# If s ≠ 0 or s ≠ n − r，output signature = (r, s)
if(s!=0 or s!=n-r):
    print("signature:")
    print(hex(r))
    print(hex(s))

# 关闭连接
bob.close()
print("Alice close.")





