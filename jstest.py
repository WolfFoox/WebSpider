# 在python中导入js代码运行
import subprocess
from functools import partial
subprocess.Popen = partial(subprocess.Popen, encoding='utf-8') # 临时使用更改
import execjs
# # 方式一：使用js文件来保存js代码，在python中可以使用
# with open(r'j1.js', 'r', encoding='utf-8') as f:
#     js_data = f.read()
# # 然后再使用execjs模块的compile()函数把js代码转为python代码对象
# data = execjs.compile(js_data)
# # 最后使用 python代码对象.call('函数名')
# result = data.call('ot1',9,8)
# print(result)

# 方式二：直接用字符串来接收js代码写到py文件内部
# js_data = '''
# function ot1(x,y) {
#     console.log(x+y)
#     return x+y
# }
# '''
# data = execjs.compile(js_data)
# result = data.call('ot1',9,8)
# print(result)

# # 编码伪加密-base64字符串：
# import base64
# # 加密：
# a = '我是中国人'
# # 先转为二进制，再转为base64的字符串
# data_b64 = base64.b64encode(a.encode('utf-8'))
# print(data_b64)
# # 解密：
# # 先解码base64字符串，再解码二进制
# data = base64.b64decode(data_b64).decode('utf-8')
# print(data)

# 需要安装的加密算法库是==》 Crypto模块
# 可逆加密-对称加密（AES和DES）：
'''
进行加密算法操作的步骤一般是4步：
*   1、把要加密的明文数据、密钥转为二进制数据，再传给算法对象；
*   2、然后设置对应算法的加密模式和填充物的参数，再传给算法对象；
*   3、然后构建算法对象，并把四个部分传进去执行加密，
*   4、最后把加密出来的数据再进行转码操作（第三层加密），得出的字符串数据才可以在互联网中进行传输、存储和打印。

'''
# from Crypto.Cipher import AES      # 导入加密模块AES或DES
# from Crypto.Util.Padding import pad, unpad    # 导入填充方法和清除方法
# import base64
# # 把要加密的明文数据、密钥,初始化向量转为二进制数据
# data = '我是中国人'.encode('utf-8')
# key = '1234567890zxcvbn'.encode('utf-8')
# iv = '0987654321mnbvcx'.encode('utf-8')
# # 加密：
# # 创建加密对象，并传入参数:AES.new(key=密钥, mode=AES.MODE_模式, iv)
# AES_dict = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
# # 再把明文进行填充处理：
# pad_data = pad(data, AES.block_size)
# # 然后使用算法对象对填充后的明文二进制数据进行加密操作：
# AES_en = AES_dict.encrypt(pad_data)
# # 最后需要进行base64字符串的转码：
# AES_en_data = base64.b64encode(AES_en)
# print(AES_en_data.decode('utf-8'))
# # 解密：
# # 先创建算法对象，并传入参数
# AES_dict = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
# # 先解base84:
# AES_de = base64.b64decode(AES_en_data)
# # 再解AES：
# AES_de_data = AES_dict.decrypt(AES_de)
# # 最后去除填充物：
# unpad_data = unpad(AES_de_data,AES.block_size)
# print(unpad_data.decode('utf-8'))

# 不可逆加密-MD5和SHA1算法（签名算法）：
# md5和sha1的加密函数是由hashlib模块提供，直接导入就可以
import hashlib
data ='我是中国人'.encode('utf-8')
# md5加密：
# 先创建算法对象：
md5_dict = hashlib.md5()
# 再执行加密：
md5_dict.update(data)
# 最后需要把这个密文转为16进制字符串，才能进行打印和传输
md5_en_data = md5_dict.hexdigest()
print(md5_en_data)
