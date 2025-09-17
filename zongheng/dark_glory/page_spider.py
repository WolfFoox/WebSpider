import requests,time,random,sys, re
from lxml import etree
sys.path.append('../..')
from Error_handle import error_handing

def get_urllist_urlnamelist()->tuple:
    url = 'https://www.zongheng.com/detail/1366535?tabsName=catalogue'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url, headers=headers, timeout=3)
    with open('最强狂兵Ⅱ：黑暗荣耀首页.html', 'w+', encoding='utf-8') as f:
        f.write(res.text)
    html = etree.HTML(res.text)
    url_list = html.xpath('//a[@class="book-info--btn-reading book-info--btn-base"]/@href')[0]
    url_list = 'https:' + url_list
    latest_chapter = re.findall('latestChapterName:"(.*?)"',res.text)[0]
    total_chapter = int(re.findall('\d+',latest_chapter)[0])
    return url_list, total_chapter

def get_url(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url, headers=headers, timeout=3)
    html = etree.HTML(res.text)
    url ='https://read.zongheng.com' + html.xpath('//a[text()="下一章"]/@href')[0]
    return url
@error_handing.get_error
def get_data(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url, headers=headers, timeout=3)
    html = etree.HTML(res.text)
    urlname = html.xpath('//div[@class="title_txtbox"]//text()')[0]
    content_text = html.xpath('//div[@class="content"]//text()')
    with open(f'{urlname}.html', 'w+', encoding='utf-8') as f:
        f.write(res.text)
    with open(f'{urlname}.txt', 'w+', encoding='utf-8') as f:
        f.writelines(content_text)
    return res.status_code

if __name__ == '__main__':
    url, total_chapter = get_urllist_urlnamelist()
    n = int(input(f'请输入需要爬取的章节数（总共有{total_chapter}章）:'))
    for i in range(n):
        get_data(url=url)
        url = get_url(url=url)
        time.sleep(random.randint(1,3))
