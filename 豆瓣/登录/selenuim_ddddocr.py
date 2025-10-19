# Pyspider133788388@$
# 豆瓣-iframe区域滑块验证码处理：
# import time, ddddocr
#
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver import ActionChains
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
# driver.get('https://www.douban.com/')
# time.sleep(3)
# # 定位到【密码登录】的区域，去填写基本信息，点击登录按钮：
# # 先切换到登录的iframe区域窗口==》驱动对象.switch_to.frame(iframe元素对象)
# driver.switch_to.frame(driver.find_element(By.XPATH, '//div[@class="login"]//iframe'))
# # 然后再点击进入到【密码登录】的区域：
# driver.find_element(By.XPATH, '//li[@class="account-tab-account"]').click()
# time.sleep(2)
# driver.find_element(By.ID, 'username').send_keys('13378838824')
# driver.find_element(By.ID, 'password').send_keys('Pyspider133788388@$')
# driver.find_element(By.LINK_TEXT, '登录豆瓣').click()
# time.sleep(3)
# '=======================提取滑块相关图片===================================='
# # 先切换到新增出来的滑块的iframe区域窗口==》驱动对象.switch_to.frame(iframe元素对象)
# driver.switch_to.frame(driver.find_element(By.ID, 'tcaptcha_iframe_dy'))
# # 下载缺口背景图片：
# yzm_bg_img = driver.find_element(By.ID, 'slideBg')
# time.sleep(2)
# yzm_bg_img.screenshot('缺口背景图片.png')
# # 下载滑块小图片
# yzm_small_img = driver.find_element(By.XPATH, '//div[@class="tc-fg-item"]')
# time.sleep(2)
# yzm_small_img.screenshot('滑块小图片.png')
# '=======================识别滑块缺口位置===================================='
# ocr = ddddocr.DdddOcr(det=False, ocr=False)  # 这里的两个参数表示不进行文本区域的检测，只识别图像
# with open('缺口背景图片.png','rb') as f:
#     bg_bytes = f.read()
# with open('滑块小图片.png','rb') as f:
#     target_bytes = f.read()
#
# result = ocr.slide_match(target_bytes, bg_bytes, simple_target=True)
# print(result) # {'target_x': 0, 'target_y': 0, 'target': [20, 63, 70, 113]}
# # 提取基本距离出来，该距离需要后续进行测试调整：
# distance = result.get('target')[0]+20 # 左右两边的滑块图片中滑块与图片边缘的距离，自己估算
'=======================设置移动轨迹，进行模拟拖动滑块===================================='
'''
selenium中鼠标动作链相关方法：
    1、先构建动作链对象==》用来封装一系列动作；
        shubiao = webdriver.ActionChains(驱动对象)
    2、然后设置一系列动作：
        - 动作链对象.click(元素对象)==》对元素进行右击；
        - 动作链对象.double_click(元素对象)==》对元素进行双击；
        - 动作链对象.click_and_hold(元素对象)==》对元素单击按住不放；
        - 动作链对象.move_by_offset(xoffset=x, yoffset=y)==>
        鼠标按给出的偏移值进行移动，x表示水平方向（正数为右），y表示垂直方向
        - 动作链对象.pause(秒数)==》设置动作之间的时间间隔；
        - 动作链对象.release()==》放开鼠标。
    3、最后需要去执行所有动作==》动作链对象.perform()
'''
# shubiao = webdriver.ActionChains(driver)
# # 下面是一些动作的设置
# slide = driver.find_element(By.XPATH, '//div[@class="tc-fg-item tc-slider-normal"]')
# shubiao.click_and_hold(slide)  # 按住滑块不放
# shubiao.pause(0.2)
# shubiao.move_by_offset(xoffset=distance+80, yoffset=0)  # 水平方向移动140，垂直方向不动
# shubiao.pause(1.5)
# shubiao.move_by_offset(xoffset=-10, yoffset=0)
# shubiao.pause(0.8)
# shubiao.release()
# shubiao.perform()

import time, ddddocr

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
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
driver.get('https://www.douban.com/')
time.sleep(3)
# 定位到【密码登录】的区域，去填写基本信息，点击登录按钮：
# 先切换到登录的iframe区域窗口==》驱动对象.switch_to.frame(iframe元素对象)
driver.switch_to.frame(driver.find_element(By.XPATH, '//div[@class="login"]//iframe'))
# 然后再点击进入到【密码登录】的区域：
driver.find_element(By.XPATH, '//li[@class="account-tab-account"]').click()
time.sleep(2)
driver.find_element(By.ID, 'username').send_keys('13378838824')
driver.find_element(By.ID, 'password').send_keys('Pyspider133788388@$')
driver.find_element(By.LINK_TEXT, '登录豆瓣').click()
time.sleep(3)
'=======================提取滑块相关图片===================================='
# 先切换到新增出来的滑块的iframe区域窗口==》驱动对象.switch_to.frame(iframe元素对象)
driver.switch_to.frame(driver.find_element(By.ID, 'tcaptcha_iframe_dy'))
while True:
    try:
        # 下载缺口背景图片：
        yzm_bg_img = driver.find_element(By.ID, 'slideBg')
        time.sleep(2)
        yzm_bg_img.screenshot('缺口背景图片.png')
        # 下载滑块小图片
        yzm_small_img = driver.find_element(By.XPATH, '//div[@class="tc-fg-item"]')
        time.sleep(2)
        yzm_small_img.screenshot('滑块小图片.png')
        '=======================识别滑块缺口位置===================================='
        ocr = ddddocr.DdddOcr(det=False, ocr=False)  # 这里的两个参数表示不进行文本区域的检测，只识别图像
        with open('缺口背景图片.png','rb') as f:
            bg_bytes = f.read()
        with open('滑块小图片.png','rb') as f:
            target_bytes = f.read()

        result = ocr.slide_match(target_bytes, bg_bytes, simple_target=True)
        print(result) # {'target_x': 0, 'target_y': 0, 'target': [20, 63, 70, 113]}
        # 提取基本距离出来，该距离需要后续进行测试调整：
        distance = result.get('target')[0]+5 # 左右两边的滑块图片中滑块与图片边缘的距离，自己估算

        shubiao = webdriver.ActionChains(driver)
        # 下面是一些动作的设置
        slide = driver.find_element(By.XPATH, '//div[@class="tc-fg-item tc-slider-normal"]')
        shubiao.click_and_hold(slide)  # 按住滑块不放
        shubiao.pause(0.2)
        shubiao.move_by_offset(xoffset=distance+100, yoffset=0)  # 水平方向移动140，垂直方向不动
        shubiao.pause(1.5)
        shubiao.move_by_offset(xoffset=-10, yoffset=0)
        shubiao.pause(0.8)
        shubiao.release()
        shubiao.perform()
        time.sleep(2)
        # 定位到切换图片的图标，点击切换一张
        driver.find_element(By.XPATH, '//img[@class="tc-action-icon unselectable"]').click()
    except Exception as e:
        break
    else:
        time.sleep(2)