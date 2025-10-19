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
driver.get('https://passport.vivo.com.cn/#/login?lang=zh_CN')
time.sleep(3)

driver.find_element(By.XPATH, '//span[text()="密码登录"]').click()
time.sleep(2)
driver.find_elements(By.CSS_SELECTOR, '.input')[3].send_keys('13378838824')
driver.find_elements(By.CSS_SELECTOR, '.input')[4].send_keys('VivoSpider2025')
driver.find_element(By.CSS_SELECTOR,'.os-pc-btn').click()
ocr = ddddocr.DdddOcr(det=False, ocr=False)  # 这里的两个参数表示不进行文本区域的检测，只识别图像
time.sleep(6)
while True:
    try:
        img_src = driver.execute_script('return document.querySelector("#dx_captcha_basic_bg_1>canvas").toDataURL("image/png")')
        img_base64 = img_src.split(',')[1]
        img_bytes = base64.b64decode(img_base64)
        with open(r'vivo缺口背景图.png','wb+') as f:
            f.write(img_bytes)

        target_img = driver.find_element(By.XPATH, '//div[@id="dx_captcha_basic_sub-slider_1"]//img')
        time.sleep(2)
        target_img.screenshot('vivo小滑块图片.png')
        # 2、使用ddddocr识别滑块位置
        with open('vivo小滑块图片.png','rb') as f:
            target_bytes = f.read()

        result = ocr.slide_match(target_bytes, img_bytes, simple_target=True)
        print(result)
        distance = result.get('target')[0]
        # 3、设置移动轨迹
        shubiao = webdriver.ActionChains(driver)
        # 下面是一些动作的设置
        slide = driver.find_element(By.ID, 'dx_captcha_basic_slider-img-normal_1')
        shubiao.click_and_hold(slide)  # 按住滑块不放
        shubiao.pause(0.2)
        shubiao.move_by_offset(xoffset=distance, yoffset=0)  # 水平方向移动140，垂直方向不动
        shubiao.pause(1.5)
        shubiao.move_by_offset(xoffset=-50, yoffset=0)
        shubiao.pause(0.8)
        shubiao.release()
        shubiao.perform()
        time.sleep(2)
        driver.find_element(By.ID, 'dx_captcha_basic_btn-refresh_1').click()
    except Exception as e:
        break
    else:
        time.sleep(2)