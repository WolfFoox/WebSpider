import time, ddddocr, base64

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
driver.get('https://demos.geetest.com/slide-bind.html')
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
# 在新出来的滑块区域中去定位对应的相关图片的标签：三个canvas标签是怀疑对象，可以全部下载下来
'''
canvas元素步骤提取图片url和数据的步骤：
    1、通过执行Js编程语言中的定位函数去定位到canvas元素，
    2、再使用Js语言的toDataURL()函数提取出对应的url数据出来；
    3、再把这个元素的base64数据转为二进制数据，进行下载为文件保存。
'''
def get_img_bytes(js_data, file_name):
    # 在python中是使用excute_script()函数来执行js代码的，
    # 如果需要执行的结果可以被返回出来，就需要在js代码的前面加一个renturn关键字
    js = f'return document.getElementsByClassName("{js_data}")[0].toDataURL("image/png")'
    img_base64 = driver.execute_script(js)
    img_base64_split = img_base64.split(',')[1]
    img_bytes = base64.b64decode(img_base64_split)  # 转换为二进制数据
    with open(rf'{file_name}','wb+') as f:
        f.write(img_bytes)
    return img_bytes

img1_bytes = get_img_bytes('geetest_canvas_bg geetest_absolute','canvas1.png')
img2_bytes = get_img_bytes('geetest_canvas_slice geetest_absolute','canvas2.png')
img3_bytes = get_img_bytes('geetest_canvas_fullbg geetest_fade geetest_absolute','canvas3.png')
# 识别出缺口位置信息：
ocr = ddddocr.DdddOcr(det=False, ocr=False)  # 这里的两个参数表示不进行文本区域的检测，只识别图像
result = ocr.slide_comparison(img1_bytes, img3_bytes)
print(result)  # {'target': [112, 84]}
# 因为滑块没有直接挨着图片的边界，所以真正移动的距离需要自己调节一下：
distance = result.get("target")[0] - 2

shubiao = webdriver.ActionChains(driver)
# 下面是一些动作的设置
slide = driver.find_element(By.XPATH, '//div[@class="geetest_slider_button"]')
shubiao.click_and_hold(slide)  # 按住滑块不放
shubiao.pause(0.2)
shubiao.move_by_offset(xoffset=distance, yoffset=0)  # 水平方向移动140，垂直方向不动
shubiao.pause(1.5)
shubiao.move_by_offset(xoffset=-2, yoffset=0)
shubiao.pause(0.8)
shubiao.release()
shubiao.perform()
time.sleep(2)



