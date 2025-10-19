# import requests, ddddocr
#
# def get_img_url():
#     url = 'http://www.fbook.net/Member/Login'
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
#     }
#
#     res = requests.get(url=url,headers=headers,verify=False)
#
#     img_url = 'http://www.fbook.net'+'/Member/Captcha?t=636232940022839332'
#
#     return  img_url
#
# def download_img(img_url)->str:
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
#     }
#
#     res = requests.get(url=img_url,headers=headers,verify=False)
#
#     with open('验证码.jpg','wb+') as f:
#         f.write(res.content)
#     # 解析器：解析出图片中的文字
#     ocr = ddddocr.DdddOcr(show_ad=False, beta=False)
#     captcha = ocr.classification(res.content)
#     return captcha
#
# def denlu(captcha)->str:
#     url = 'http://www.fbook.net/Member/Login'
#
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
#         'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'
#     }
#
#     data = f'loginName=13378838824&loginPass=pyspider&captcha={captcha}'
#     res = requests.post(url=url,headers=headers,data=data,verify=False)
#
#     token = res.cookies.get('max')
#
#     return token
#
# def data(token):
#     url = 'http://www.fbook.net/'
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
#         'cookie': f'max={token}'
#     }
#     res = requests.get(url=url,headers=headers,verify=False)
#
#     with open('天下书盟首页登录页面.html','w+',encoding='utf-8') as f:
#         f.write(res.text)
#
#
# if __name__ == '__main__':
#     img_url = get_img_url()
#     captcha = download_img(img_url)
#     token = denlu(captcha)
#     data(token)


# selenium自动化结合ddddocr来破解登录规则-图片字符验证码登录：
# 有界面模式：调试
# import time, ddddocr
#
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# options = webdriver.ChromeOptions()   # 在创建驱动对象并启动浏览器之前可以先添加一些对浏览器的设置
# # 去掉打开浏览器自动出现的指痕提升
# options.add_experimental_option('excludeSwitches', ['enable-automation'])
# options.add_experimental_option('useAutomationExtension', False)
# options.add_argument(f'--disable-extensions') # 禁用浏览器的一些拓展程序（防止有些网站打不开）
# options.add_experimental_option('detach',True) # 禁止浏览器自动关闭
#
# driver = webdriver.Chrome(options=options)
# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#     'source': '''
#     Object.defineProperty(navigator, "webdriver", {get:() => false})
#     '''
# })
# driver.get('http://www.fbook.net/Member/Login/')
# time.sleep(3)
# driver.find_element(By.ID, 'loginName').send_keys('13378838824')
# driver.find_element(By.ID, 'loginPass').send_keys('pyspider')
# time.sleep(2)
# '==========================验证码的识别==================================='
# # 定位到验证码图片，并截图获取它的二进制数据
# yzm_bytes = driver.find_element(By.ID, 'ImageCheck').screenshot_as_png
# # 使用ddddocr库的方法识别图片中的文字：
# ocr = ddddocr.DdddOcr(show_ad=False, beta=True)
# yzm_data = ocr.classification(yzm_bytes)
# driver.find_element(By.ID, 'captcha').send_keys(yzm_data)
# # 定位到登录按钮，单击进行登录：
# driver.find_element(By.ID,'js-submit-login').click()
# time.sleep(3)
#
# # 切换到当前页面中的警示框窗口的方法==》驱动对象.switch_to.alert
# alert = driver.switch_to.alert
# # 点击确定按钮==》警示框窗口对象.accept()
# alert.accept()


# 无限流
import time, ddddocr

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
driver.get('http://www.fbook.net/Member/Login/')
time.sleep(3)
driver.find_element(By.ID, 'loginName').send_keys('13378838824')
driver.find_element(By.ID, 'loginPass').send_keys('pyspider')
time.sleep(2)
'==========================验证码重试机制==================================='
while True:
    # 定位到验证码图片，并截图获取它的二进制数据
    yzm_bytes = driver.find_element(By.ID, 'ImageCheck').screenshot_as_png
    # 使用ddddocr库的方法识别图片中的文字：
    ocr = ddddocr.DdddOcr(show_ad=False, beta=True)
    yzm_data = ocr.classification(yzm_bytes)
    yzm_input = driver.find_element(By.ID, 'captcha')
    yzm_input.send_keys(yzm_data)
    # 定位到登录按钮，单击进行登录：
    driver.find_element(By.ID,'js-submit-login').click()
    time.sleep(3)

    # 切换到当前页面中的警示框窗口的方法==》驱动对象.switch_to.alert
    alert = driver.switch_to.alert
    # 获取警示框的文本==》警示框窗口对象.text
    if alert.text == '登录成功':  # 验证码识别正确登录成功，就退出无限流模式
        # 点击确定按钮==》警示框窗口对象.accept()
        alert.accept()
        break
    else:
        # 点击确定按钮==》警示框窗口对象.accept()
        alert.accept()
        yzm_input.clear()  # 清空
        driver.find_element(By.LINK_TEXT, '看不清？换一个!').click()  # 点击换一张
        time.sleep(3)






