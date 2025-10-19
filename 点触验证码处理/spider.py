import time, ddddocr, base64, requests, re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from chaojiying import Chaojiying_Client
options = webdriver.ChromeOptions()   # 在创建驱动对象并启动浏览器之前可以先添加一些对浏览器的设置
# 去掉打开浏览器自动出现的指痕提升
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument(f'--disable-extensions') # 禁用浏览器的一些拓展程序（防止有些网站打不开）
options.add_experimental_option('detach',True) # 禁止浏览器自动关闭

driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    'source': '''
    Object.defineProperty(navigator, "webdriver", {get:() => false})
    '''
})
driver.get('https://demos.geetest.com/click-bind.html')
time.sleep(3)

yhm = driver.find_element(By.ID, 'username')
yhm.clear()
yhm.send_keys('xiaolang')
mm = driver.find_element(By.ID, 'password')
mm.clear()
mm.send_keys('123456')
time.sleep(2)
driver.find_element(By.ID, 'btn').click()
time.sleep(2)

bg_div_style = driver.find_element(By.CLASS_NAME, 'geetest_item_wrap').get_attribute('style')
# print(bg_div_style)
img_url = re.search('"(.*)"', bg_div_style).group(1)
print(img_url) # https://static.geetest.com/captcha_v3/custom_batch/v3/85/2024-01-26T18/icon/c754bf4118b24e00a564f84e566535ae.jpg?challenge=50f184612c9ec15ae78edaecd1fc4097
header = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }

res = requests.get(url=img_url,headers=header)

with open(rf'点触验证码背景图.jpg','wb+') as f:
    f.write(res.content)

# 识别图形的位置信息
# 构建超级鹰的连接对象：需要提供三个参数‘用户名’、‘密码’、‘软件id'
cjy = Chaojiying_Client('SuperShark', 'f13pm7qn', '973685')
# 提取出要识别图片的二进制出来：
result = cjy.PostPic(res.content, 9103).get("pic_str")
print(result)
position_all = [i.split(',') for i in result.split('|')]
print(position_all)  #
# 设置点击轨迹：
# selenium中移动鼠标到具体元素的动作函数为==》 动作链对象.move_to_element_wit_offset(图片对象, 水平方向需要移动的距离, 垂直方向需要移动的距离)
bg_img = driver.find_element(By.CLASS_NAME, 'geetest_item_wrap')
for i in position_all:
    shubiao = webdriver.ActionChains(driver)
    # selenium的坐标基点是在图片的正中心，相当于鼠标也是从正中心去移动，
    # 而识别工具识别出来的是x和y的距离是从左上角识别的（相当于顶部），所以真实要移动的距离是：|识别的距离|-图片长度或宽度的一半
    # selenium中去获取元素高和宽的函数为==》元素对象.rect('width')、元素对象.rect('height')
    x = int(i[0])-bg_img.rect["width"]/2
    y = int(i[1])-bg_img.rect["height"]/2
    shubiao.move_to_element_with_offset(bg_img, x, y).click()  # 移动到图标进行点击
    shubiao.perform()
    time.sleep(2)

driver.find_element(By.CLASS_NAME, 'geetest_commit_tip').click()


