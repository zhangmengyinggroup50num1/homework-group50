from gmssl import sm3
import gmssl
import struct

# 构造合法的哈希值
def construct_hash(original_message, extension_message):
    
    return sm3.sm3_hash(list(original_message+padding+extension_message))

# 长度扩展攻击
def length_extension_attack(original_message,  extension_message):
    hash_value=sm3.sm3_hash(list(original_message))
    # 构造合法的哈希值和伪造的消息
    forged_hash = construct_hash(original_message,extension_message )
    
    
   
    forged_message = original_message +padding+ extension_message

    print("原始消息: ", original_message)
    print("原始哈希: ", hash_value)
    print("伪造消息: ", forged_message)
    print("伪造哈希: ", forged_hash)

# 测试样例
original_message = b'Hello, world!'
original_hash = sm3.sm3_hash(list(original_message))
extension_message = b' This is an extension.'
length = len(original_message) + 8
padding = b'\x80' + b'\x00' * ((56 - length) % 64) + struct.pack('>Q', length * 8)
length_extension_attack(original_message,  extension_message)
