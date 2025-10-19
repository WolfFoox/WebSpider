# selenium自动化操作：
'''
基础操作
    1、先使用对应浏览器的驱动函数去创建驱动对象并打开浏览器
    2、再通过驱动对象去打开要操作的网页页面
    3、然后就可以使用驱动对象提供的或者其他模块提供的方法或属性具体‘交互’
'''
# import time
#
# from selenium import webdriver
# options = webdriver.ChromeOptions()   # 在创建驱动对象并启动浏览器之前可以先添加一些对浏览器的设置
# options.add_argument('--start-maximized') # 最大化窗口
# options.add_argument(f'--proxy-server={ip}') # 设置代理ip
# options.add_argument(f'--incognito') # 无痕浏览，但是表面上的无痕（清除浏览历史记录），但后台一般会有显示（加不加无所谓）
# options.add_argument(f'--disable-extensions') # 禁用浏览器的一些拓展程序（防止有些网站打不开）
# options.add_experimental_option('detach',True) # 禁止浏览器自动关闭


'************************************webdriver常用属性和方法*************************'
'''

webdriver.Chrome()    ==>创建谷歌的驱动对象（并打开浏览器）
驱动对象.get('网址')     ==>打开指定的网址
驱动对象.current_url    ==>获取当前页面的url
驱动对象.title          ==>获取当前页面的标题
驱动对象.page_source    ==>获取当前页面的源代码（html）
驱动对象.window_handles ==>获取所有打开页面的句柄（html）
驱动对象.current_window_handles    ==>获取当前页面的句柄（html）

'''

# driver = webdriver.Chrome(options=options) # 带着浏览器的相关设置创建驱动对象并打开浏览器
# driver.get('https://www.baidu.com')  # 驱动对象去打开百度一下的网页
# data_url = driver.current_url
# data_title = driver.title
# data = driver.page_source
# with open(r'网址备份.txt','w+',encoding='utf-8') as f:
#     f.write(f'{data_title}:{data_url}')
# with open(rf'{data_title}.html','w+',encoding='utf-8') as f:
#     f.write(data)

# 因为当进程结束时，selenium开启的浏览器就会自动关闭，
# 如果想要浏览器界面停留长一点的时间可以使用time模块去休眠进程
# import time
# time.sleep(10)

'************************************元素的定位和获取*************************'
# driver = webdriver.Chrome(options=options) # 带着浏览器的相关设置创建驱动对象并打开浏览器
# driver.get('https://www.baidu.com')  # 驱动对象去打开百度一下的网页
# 可以导入selenium中提供的定位的类==》 By
from selenium.webdriver.common.by import By
'''
单个元素定位：
    - 驱动对象.find_element(By.ID, 'id值')==》通过id值定位到元素并获取对象
    - 驱动对象.find_element(By.CLASS_NAME, 'class值')==》通过class值定位到元素并获取对象
    - 驱动对象.find_element(By.NAME, 'name值')==》通过name值定位到表单控件元素并获取对象
    - 驱动对象.find_element(By.TAG_NAME, '标签名')==》通过标签名定位到元素并获取对象
    - 驱动对象.find_element(By.XPATH, 'xpath表达式')==》通过xpath表达式定位到元素并获取对象
    - 驱动对象.find_element(By.PARTISL_LINK_TEXT, '内容区部分文字')==》通过标签内容区的模糊文本定位到元素并获取对象
多个元素定位：
    把find_element改成find_elements就可以获取到所有匹配到的元素，结果是一个列表
'''
'''
元素标签的信息获取：
    - 元素对象.get_attribute('属性名')==》提取元素的某个属性值
    - 元素对象.tag_name==》提取元素的标签名
    - 元素对象.text==》提取元素的内容区的文本
    - 元素对象.location==》提取元素的位置
    - 元素对象.size==》提取元素的大小
'''
# rs = driver.find_element(By.XPATH,'//span[@class="title-content-title"]')
# data = rs.text
# print(data)
'************************************交互操作（事件处理）*************************'
'''
页面交互的操作，常用的有9种：
    - 键盘操作（输入）
    - 鼠标操作（点击）
    - 清除
    - 提交
    - 等待
    - js执行
    - 当前页面的前进后退
    - 切换窗口
    - 关闭浏览器
'''

'===========================键盘操作====================================='
# 键盘输入文字==》 元素对象.send_keys('文字')
from selenium.webdriver.common.keys import  Keys  # 导入键盘上的各种键
from selenium.webdriver.support.ui import WebDriverWait  # 这个是显示等待的类
from selenium.webdriver.support import expected_conditions as EC   # 这个是显式等待进行定位的模块
'''
元素对象.send_keys(Keys.BACK_SPACE)==> 按删除键
元素对象.send_keys(Keys.SPACE)==> 按空格键
元素对象.send_keys(Keys.TAB)==> 按制表键
元素对象.send_keys(Keys.ENTER)==> 按回车键
元素对象.send_keys(Keys.CONTROL, 'a')==> 全选ctrl+a
元素对象.send_keys(Keys.CONTROL, 'c')==> 复制ctrl+c
元素对象.send_keys(Keys.CONTROL, 'v')==> 粘贴ctrl+v
元素对象.send_keys(Keys.CONTROL, 'x')==> 剪切ctrl+x
元素对象.send_keys(Keys.CONTROL, 'z')==> 撤销ctrl+z
'''
# baidu_input = driver.find_element(By.ID,'kw')
# wait = WebDriverWait(driver, 10)
# baidu_input = wait.until(EC.element_to_be_clickable((By.ID, 'kw')))
# baidu_input.send_keys('小说')
# baidu_input.send_keys(Keys.ENTER)
# time.sleep(3)   # 等待页面加载
# with open(rf'{driver.title}.html','w+',encoding='utf-8') as f:
#     f.write(driver.page_source)
#
# # 重新定位元素后再执行Ctrl+A
#
# baidu_input = wait.until(EC.element_to_be_clickable((By.ID, 'chat-textarea')))
# baidu_input.send_keys(Keys.CONTROL,'a')
# baidu_input.send_keys(Keys.BACK_SPACE)
# baidu_input.send_keys('湖南')
# baidu_input.send_keys(Keys.ENTER)
# with open(rf'{driver.title}.html','w+',encoding='utf-8') as f:
#     f.write(driver.page_source)

'===========================鼠标操作====================================='
'''
元素对象.click()   ==>鼠标左键单击
元素对象.context_click()   ==>鼠标右键单击
元素对象.double_click()   ==>鼠标左键双击
元素对象.move_to_element()   ==>鼠标悬停
'''
# baidu_input = driver.find_element(By.ID,'kw')
# # wait = WebDriverWait(driver, 10)
# # baidu_input = wait.until(EC.element_to_be_clickable((By.ID, 'kw')))
# baidu_input.send_keys(input('请输入你的搜索关键字：'))
# submit = driver.find_element(By.ID,'su')
# submit.click()  #单击百度一下按钮

'===========================鼠标操作====================================='
# baidu_input = driver.find_element(By.ID,'kw')
# wait = WebDriverWait(driver, 10)
# baidu_input = wait.until(EC.element_to_be_clickable((By.ID, 'kw')))
# baidu_input.send_keys(input('请输入你的搜索关键字：'))
# submit = driver.find_element(By.ID,'su')
# submit.click()  #单击百度一下按钮
# time.sleep(3)   # 等待页面加载
# with open(rf'{driver.title}.html','w+',encoding='utf-8') as f:
#     f.write(driver.page_source)
#
# while True:
#     choice = input('请输入是否继续爬取（y/n）:')
#     if choice == 'y':
#         baidu_input.clear()  # 清除关键字
#         # n = input('请输入关键字：')
#         baidu_input.send_keys(input('请输入你的搜索关键字：'))
#         baidu_input.submit()
#         time.sleep(3)
#         with open(rf'{driver.title}.html', 'w+', encoding='utf-8') as f:
#             f.write(driver.page_source)
#     else:
#         print('感谢您的使用')

'===========================设置等待加载操作====================================='
'''
等待有三种
    - 进程中等待==》 使用time.sleeo(秒)来等待页面加载
    -隐式等待==》 需要在get()打开页面设置，对页面所有元素起效==》驱动对象.implicitly_wait(秒)
    - 显式等待==》在get()打开页面后设置，只针对某个元素
        ==》先创建等待对象--》wait = WebDriverWait(驱动对象, 6)
        ==>进行元素定位并等待-->wait.until(EC.presence_of_element_located(By.方法,'方法的值'))
'''
# driver = webdriver.Chrome(options=options) # 带着浏览器的相关设置创建驱动对象并打开浏览器
#
# driver.get('https://www.baidu.com')  # 驱动对象去打开百度一下的网页
# time.sleep(3)

'===========================js执行====================================='
# wait = WebDriverWait(driver, 10)
# baidu_input = wait.until(EC.element_to_be_clickable((By.ID, 'chat-textarea')))
# baidu_input = driver.find_element(By.ID,'chat-textarea')
# baidu_input.send_keys('小说')
# baidu_input.send_keys(Keys.ENTER)
# time.sleep(3)
# # 写js代码进行鼠标滑轮滚动到距离顶部2000的位置（这样滚轮就一定会滚到最下面）
# js = 'document.documentElement.scrollTop=2000'
# # 执行js代码的函数是==》 驱动对象.execute_script('js代码')
# driver.execute_script(js)
# time.sleep(2)
# n = driver.find_element(By.CLASS_NAME, 'rightArrow_2RcSz')   # 定位到‘下一页’的按钮
# n.click()

'===========================页面和窗口的切换====================================='
# 页面的回退（返回到上一页）的函数为==》 驱动对象.back()
# 页面的前进（进入到下一页）的函数为==》 驱动对象.forward()
# time.sleep(3)
# driver.back()
# time.sleep(2)
# driver.forward()

'===========================窗口的切换====================================='
# 在浏览器中进行窗口的切换函数是==》 驱动对象.switch_to.window(窗口句柄)
# for i in range(10):
#     li1 = driver.find_element(By.XPATH, f'//li[@data-index="{i}"]')  # 定位到第一个热搜
#     li1.click()
#     time.sleep(2)
#     cwh = driver.current_window_handle
#     wh = driver.window_handles   # 拿到所有窗口的句柄
#     driver.switch_to.window(wh[0])  #  选中‘百度一下’（就是第一个窗口）的句柄切换过去
#     time.sleep(3)

'===========================关闭浏览器====================================='
# driver.quit()   # 做完任务手动关闭

'********************************避免检测到自动化*****************************************'
'''
有界面操作浏览器的模式?什么时候用无界面模式？
    - 有界面操作浏览器的模式可以用于【调试】第一次的网站的自动化操作，来避免出现各种问题；
    - 无界面操作浏览器的模式是用于【最终程序】的反复执行。
    原因是：有界面需要加载很多的画面，导致需要大量的资源，就会导致爬取的速率和效率都比较低
'''
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# options = webdriver.ChromeOptions()   # 在创建驱动对象并启动浏览器之前可以先添加一些对浏览器的设置
# # options.add_argument('--start-maximized') # 最大化窗口
# # options.add_argument(f'--proxy-server={ip}') # 设置代理ip
# # options.add_argument(f'--incognito') # 无痕浏览，但是表面上的无痕（清除浏览历史记录），但后台一般会有显示（加不加无所谓）
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
# driver.get('https://www.baidu.com')

"===================================无界面模式===================================="
'''
无界面在options对象中一般是设置以下的参数：
    - options.add_argument('--headless')==> 无界面浏览
    - options.add_argument('user-agent="谷歌浏览器的版本身份"')==》 可以设置一下请求标头
    - options.add_argument('--disable-gpu')==》 selenium无头模式是默认不用无痕浏览是不需要开启GPU
    - options.add_argument('--disable-extensions')==》 禁用浏览器里拓展的开启
    - options.add_argument(f'--proxy-server={ip}') # 设置代理ip
     
'''
options = webdriver.ChromeOptions()   # 在创建驱动对象并启动浏览器之前可以先添加一些对浏览器的设置
options.add_argument('--headless')
options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"')
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')

driver = webdriver.Chrome(options=options)
driver.get('https://www.baidu.com')
time.sleep(3)

with open(rf'{driver.title}.html','w+',encoding='utf-8') as f:
    f.write(driver.page_source)

