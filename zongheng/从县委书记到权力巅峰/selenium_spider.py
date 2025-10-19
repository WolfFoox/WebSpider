# 有界面模式：调试
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
options = webdriver.ChromeOptions()   # 在创建驱动对象并启动浏览器之前可以先添加一些对浏览器的设置
# options.add_argument('--start-maximized') # 最大化窗口
# options.add_argument(f'--proxy-server={ip}') # 设置代理ip
# options.add_argument(f'--incognito') # 无痕浏览，但是表面上的无痕（清除浏览历史记录），但后台一般会有显示（加不加无所谓）
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
driver.get('https://www.zongheng.com/detail/1296249?tabsName=catalogue')
time.sleep(6)
click_count = driver.find_element(By.XPATH,"//span[contains(text(),'共')]")
chioce = int(input(f'请输入需要爬取的章节数（总{click_count.text}）:'))
new_windows = driver.find_elements(By.XPATH, '//a[@class="chapter-list--item"]')
for i in range(chioce):
    new_windows[i].click()
    time.sleep(3)
    window_handles = driver.window_handles
    c_window_handles = driver.current_window_handle
    if c_window_handles != window_handles[-1]:
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(3)
        with open(rf'{driver.title}.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
    window_handles = driver.window_handles
    driver.switch_to.window(driver.window_handles[0])

# 无界面模式：
# 修改头部设置即可

# options = webdriver.ChromeOptions()   # 在创建驱动对象并启动浏览器之前可以先添加一些对浏览器的设置
# options.add_argument('--headless')
# options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"')
# options.add_argument('--disable-gpu')
# options.add_argument('--disable-extensions')
#
# driver = webdriver.Chrome(options=options)