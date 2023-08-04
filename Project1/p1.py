from gmssl import sm3
import random
import time

# 生成随机消息
def generate_random_message(length):
    return bytes(random.choices(range(256), k=length))
    '''msg=''
    allchoice="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    for i in range(length):
        randomnum=random.randint(0,60)
        msg= msg.join(allchoice[randomnum])
    return bytes(msg)#''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(length)))
'''
# 朴素生日攻击
def birthday_attack():
    hash_dict = {} # 用字典存储已计算的哈希值及对应的输入
    collision_found = False

    while not collision_found:
        message = generate_random_message(3)
        msg_list = list(message)
        hash_value = str(sm3.sm3_hash(msg_list))

        if (hash_value in hash_dict)and (message.hex() != hash_dict[hash_value]): # 发现哈希冲突
            collision_found = True
            print("哈希冲突发现！")
            print("消息1: ", hash_dict[hash_value])#字典中该哈希值相对应的消息
            print("消息2: ", message.hex())
            print("哈希值: ", hash_value)
        else:
            hash_dict[hash_value] = message.hex()
start=time.time()
birthday_attack()
end=time.time()
print("生日攻击所用时间为：",end-start)
# Project1: implement the naïve birthday attack of reduced SM3

## 生日攻击
#用到gmssl库
#生日攻击基于生日悖论，对于长度为 $2^n$ 的hash值，只需要枚举 $2^{\frac{n}{2}}$ 次即可找到一对碰撞。

## 代码实现

#利用穷举法，将已计算的消息的hash值存储在字典中，然后随机产生消息，生成hash值后检查该hash值是否在字典中，若在，检查是否是同一条消息，若在字典中，且不是同一条消息，则找到碰撞。



## 运行结果
#经过测试，较短的信息没有碰撞，而较长的信息生日攻击找到碰撞消耗时间十分长，很难找到两个不同的消息得到完全相同的hash值


