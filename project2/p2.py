from gmssl import sm3
import random
import time

# 生成随机消息
def generate_random_message(length):
    return bytes(random.choices(range(256), k=length))
def hextoint(strings):
    dlist=[]
    for i in range(0,len(strings),2):
        num=strings[i:i+2]
        dnum=int(strings,16)
        dlist.append(dnum)
    return dlist
# rho攻击
def rho_attack():
    hash_dict = {} # 用字典存储已计算的哈希值及对应的输入
    collision_found = False
    message = generate_random_message(2)
    msg_list = list(message)
    message=message.hex()
    hash_value = str(sm3.sm3_hash(msg_list))
    while not collision_found:
 
        if (hash_value in hash_dict)and (message != hash_dict[hash_value]): # 发现哈希冲突
            collision_found = True
            print("哈希冲突发现！")
            print("消息1: ", hash_dict[hash_value])#字典中该哈希值相对应的消息
            print("消息2: ", message)
            print("哈希值: ", hash_value)
        else:
            hash_dict[hash_value] = message
            message = hash_value
            msg_list = hextoint(hash_value)
            hash_value = str(sm3.sm3_hash(msg_list))
start=time.time()
rho_attack()
end=time.time()
print("rho攻击所用时间为：",end-start)

# Project2: implement the Rho method of reduced SM3

## Rho method

#随机生成一个初始字符串，对其不断进行hash，直到找到碰撞。基本攻击方法还是穷举法，与生日攻击类似，只是从选择随机消息改为不断迭代。



## 运行结果
#经测试和生日攻击相同，较短的信息没有碰撞，而较长的信息生日攻击找到碰撞消耗时间十分长，很难找到两个不同的消息得到完全相同的hash值




