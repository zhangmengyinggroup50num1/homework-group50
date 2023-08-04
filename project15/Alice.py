import socket
from os.path import commonprefix
import math
import sys
import random 
from gmpy2 import invert
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
def mul_ECC(x,y,k):
    k = k%p
    k = bin(k)[2:]
    rx,ry = x,y
    for i in range(1,len(k)):
        rx,ry = add_ECC(rx, ry, rx, ry)
        if k[i] == '1':
            rx,ry = add_ECC(rx, ry, x, y)
    return rx%p,ry%p

p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3    
a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
X = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
Y = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
#建立连接


alice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = ('localhost', 50007)

print('Connecting to Alice...')

try:
    alice.connect(addr)
    print('successfully!')
except Exception:
    print('Failed!')
    sys.exit()



    
d2=random.randint(1,n-1)

# 接受 p1
x,addr=alice.recvfrom(1024)
x=int(x.decode(),16)
y,addr=alice.recvfrom(1024)
y=int(y.decode(),16)

#p = d2^(-1)·p1-G
p1=(x,y)
ptem=mul_ECC(p1[0],p1[1],invert(d2,p))
ptem=add_ECC(ptem[0],ptem[1],X,-Y)


# 接受 q1,e
x,addr=alice.recvfrom(1024)
x=int(x.decode(),16)
y,addr=alice.recvfrom(1024)
y=int(y.decode(),16)
q1=(x,y)
e,addr=alice.recvfrom(1024)
e=int(e.decode(),16)


k2=random.randint(1,n-1)
k3=random.randint(1,n-1)

#q2=k2·G
q2=mul_ECC(X,Y,k2)

#k3·q1+q2=(x1,y1)
x11,y11=mul_ECC(q1[0],q1[1],k3)
x11,y11=add_ECC(x11,y11,q2[0],q2[1])

# r=x1+e mod n
r=(x11+e)%n

# s2=d2*k3 mod n
s2=(d2*k3)%n

# s3=d2*(r+k2) mod n
s3=(d2*(r+k2))%n

#  r,s2,s3
alice.sendall(hex(r).encode())
alice.sendall(hex(s2).encode())
alice.sendall(hex(s3).encode())

# 关闭连接
alice.close()
print("Bob close.")






