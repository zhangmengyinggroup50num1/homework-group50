import sys
import struct
import random
from math import gcd
from math import ceil
from math import floor
from gmssl import sm3

q = "8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3"
a = "787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498"
b = "63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A"
x_G = "421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D"
y_G = "0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2"
G = (x_G, y_G)
n = "8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7"
def int_hex(str):#字符串转16进制
    return int(str, 16)


def sm3_hash(message):#求字符串的hash值
    message = message.encode('utf-8')
    msg_list = [i for i in message]
    hash_hex = sm3.sm3_hash(msg_list)

    return hash_hex


def inv(a, m):#求逆元
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def add_ECC(P, Q):#椭圆曲线加法
    if P == 0:
        return Q
    if Q == 0:
        return P
    x1, y1, x2, y2 = int_hex(P[0]), int_hex(P[1]), int_hex(Q[0]), int_hex(Q[1])
    q_int = int_hex(q)
    tmp1, tmp2 = y2 - y1, inv(x2 - x1 % q_int, q_int)
    l = tmp1 * tmp2 % q_int
    x = (l * l - x1 - x2) % q_int
    y = (l * (x1 - x) - y1) % q_int
    res = (hex(x)[2:], hex(y)[2:])
    return res


def double_ECC(P):#二倍点
    if P == 0:
        return P
    x1, y1 = int_hex(P[0]), int_hex(P[1])
    a_int, q_int = int_hex(a), int_hex(q)
    tmp1 = 3 * x1 * x1 + a_int
    tmp2 = inv(2 * y1, q_int)
    l = (tmp1 * tmp2) % q_int
    x = (l * l - 2 * x1) % q_int
    y = (l * (x1 - x) - y1) % q_int
    Q = (hex(x)[2:], hex(y)[2:])
    return Q


def mul_ECC(P, k):#点乘
    k_bin = bin(k)[2:]
    i = len(k_bin) - 1
    Q = P
    if i > 0:
        k = k - 2**i
        while i > 0:
            Q = double_ECC(Q)
            i -= 1
        if (k > 0):
            Q = add_ECC(Q, mul_ECC(P, k))

    return Q


def check_ECC(P):#检查是否在椭圆曲线上
    x, y = int_hex(P[0]), int_hex(P[1])
    q_int, a_int, b_int = int_hex(q), int_hex(a), int_hex(b)
    if (y * y) % q_int == (x * x * x + a_int * x + b_int) % q_int:
        return True
    else:
        return False


def KDF(Z, klen):#密钥扩展函数
    ct = int_hex("00000001")
    ceil_val = ceil(klen / v)
    floor_val = floor(klen / v)
    hash = b""

    for i in range(1, ceil_val):
        ct_hex = hex(ct)[2:]
        hash += sm3_hash(Z + (ct_hex).zfill(8))
        ct += 1
    ct_hex = hex(ct)[2:]
    if klen % v == 0:
        hash_x = sm3_hash(Z + (ct_hex).zfill(8))
    else:
        hash_x = sm3_hash(Z + (ct_hex).zfill(8))
        hash_x = hash_x[:((klen - v * floor_val) // 4)]
    K = hash.hex() + hash_x

    return K


def sm2_enc(M, P_B):#加密函数
    klen = len(M) * 4
    k = hex(random.randint(1,int_hex(n)-1))[2:]
    k_int = int_hex(k)
    C1 = mul_ECC(G, k_int)
    x2, y2 = mul_ECC(P_B, k_int)
    t = KDF(x2 + y2, klen)

    C2 = hex(int_hex(M) ^ int_hex(t))[2:]
    C3 = sm3_hash(x2 + M + y2)
    C = C1[0] + C1[1] + C2 + C3
    len_x = len(C1[0])
    len_y = len(C1[1])
    len_C2 = len(C2)

    return C, len_x, len_y, len_C2


def sm2_dec(CT, d_B, len_x, len_y, len_C2, klen):#解密函数
    x1 = CT[:len_x]
    y1 = CT[len_x:len_x + len_y]
    C1 = (x1, y1)
    if check_ECC(C1) == False:
        print("False!")
        return ""
    x2, y2 = mul_ECC(C1, int_hex(d_B))
    t = KDF(x2 + y2, klen)

    C2 = CT[len_x + len_y:len_x + len_y + len_C2]
    M = hex(int_hex(C2) ^ int_hex(t))[2:]

    u = sm3_hash(x2 + M + y2)
    C3 = CT[len_x + len_y + len_C2:]
    if u != C3:
        print("False!")
        return ""

    return M


#参数设定

#私钥d_B
d_B = hex(random.randint(pow(2,127),pow(2,128)))[2:]
P_B = mul_ECC(G, int_hex(d_B))
v = 256

PT = hex(random.randint(pow(2,127),pow(2,128)))[2:]
print("PT: " + PT + '\n')
klen = len(PT) * 4
CT, len_x, len_y, len_C2 = sm2_enc(PT, P_B)
print("CT: " + CT + '\n')

M = sm2_dec(CT, d_B, len_x, len_y, len_C2, klen)
print("DEC: " + M + '\n')
