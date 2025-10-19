from chaojiying import Chaojiying_Client
# 构建超级鹰的连接对象：需要提供三个参数‘用户名’、‘密码’、‘软件id'
cjy = Chaojiying_Client('SuperShark', 'f13pm7qn', '973685')
# 提取出要识别图片的二进制出来：
with open(r'img.png','rb') as f:
    img_bytes = f.read()
result = cjy.PostPic(img_bytes, 1006)
print(result)  # {'err_no': 0, 'err_str': 'OK', 'pic_id': '2302818322068290001', 'pic_str': 'ectdad', 'md5': '51d50fa280813053e6ed0ac68b64f154'}
# 识别出来是一个对象，其中的'pic_str'键的值是识别结果
data = result.get("pic_str")
print(data)   # ectdad
