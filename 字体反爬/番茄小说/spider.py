# 爬取十日终焉文字正常内容
import requests, re
from lxml import etree
from fontTools import ttLib
# 第一步==》爬取页面静态html响应数据并解析提取出‘字体文件’的url链接
def get_fonturl()->tuple:
    url = 'https://fanqienovel.com/reader/7173216089122439711'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url, headers=headers)
    with open(r'番茄小说-十日终焉第一章.html', 'w+', encoding='utf-8') as f:
        f.write(res.text)
    fonturl = re.search('src:url\((.*?)\)',res.text).group(1)
    return res.text, fonturl

# 第二步==》对字体文件的url进行请求并下载到本地：
def get_font_cmap(fonturl):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=fonturl, headers=headers)
    with open(r'font_flie.woff2','wb+') as f:
        f.write(res.content)
    # 使用fontTools库中的ttlib模块的TTFont类实例化对象去加载字体文件
    ft = ttLib.TTFont(r'font_flie.woff2')
    # 把ft字体文件对象重新保存为xml类型：
    ft.saveXML(r'font_file.xml')
    # 1、先通过xml对象（字体文件）提供的getBestCmap()函数提取出cmap标签的‘映射关系’，结果是一个字典
    cmap = ft.getBestCmap()
    # print(cmap_dict)
    # 这里是{特殊字符十进制：‘正确字符的名称’，....}
    # 因为文章响应到的正文内容里面的特殊字符是十六进制的格式，所以为了方便后面的正则查找替换数据；
    # 就需要把cmap_dict的特殊字符也转为十六进制的格式。
    cmap_dict = {}
    for key, value in cmap.items():
        # 使用python自带的hex()函数进行十进制转十六进制：
        k = hex(key)[2:]   # 这里要把0x去掉，才能在后面与响应数据去掉\u的
        cmap_dict[k] = value
    # print(cmap_dict)
    # 2、再通过xml对象（字体文件）提供的getGlyphOrder()函数提取出cmap标签的‘映射关系’，结果是一个列表
    order = ft.getGlyphOrder()[1:]  # 第一个空的字符就不需要了，取出后面
    # print(order)
    # 3、然后去FontCreator工具中把正确字符抄下来用列表来存储：
    font_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b',
                 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B',
                 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '的', '一',
                 '是', '了', '我', '不', '人', '在', '他', '有', '这', '个', '上', '们', '来',
                 '到', '时', '大', '地', '为', '子', '中', '你', '说', '生', '国', '年', '着',
                 '就', '那', '和', '要', '她', '出', '也', '得', '里', '后', '自', '以', '会',
                 '家', '可', '下', '而', '过', '天', '去', '能', '对', '小', '多', '然', '于',
                 '心', '学', '么', '之', '都', '好', '看', '起', '发', '当', '没', '成', '只',
                 '如', '事', '把', '还', '用', '第', '样', '道', '想', '作', '种', '开', '美',
                 '总', '从', '无', '情', '已', '面', '最', '女', '但', '现', '前', '些', '所',
                 '同', '日', '手', '又', '行', '意', '动', '方', '期', '它', '头', '经', '长',
                 '儿', '回', '位', '分', '爱', '老', '因', '很', '给', '名', '法', '间', '斯',
                 '知', '世', '什', '两', '次', '使', '身', '者', '被', '高', '已', '亲', '其',
                 '进', '此', '话', '常', '与', '活', '正', '感', '见', '明', '问', '力', '理',
                 '尔', '点', '文', '几', '定', '本', '公', '特', '做', '外', '孩', '相', '西',
                 '果', '走', '将', '月', '十', '实', '向', '声', '车', '全', '信', '重', '三',
                 '机', '工', '物', '气', '每', '并', '别', '真', '打', '太', '新', '比', '才',
                 '便', '夫', '再', '书', '部', '水', '像', '眼', '等', '体', '却', '加', '电',
                 '主', '界', '门', '利', '海', '受', '听', '表', '德', '少', '克', '代', '员',
                 '许', '陵', '先', '口', '由', '死', '安', '写', '性', '马', '光', '白', '或',
                 '住', '难', '望', '教', '命', '花', '结', '乐', '色', '更', '拉', '东', '神',
                 '记', '处', '让', '母', '父', '应', '直', '字', '场', '平', '报', '友', '关',
                 '放', '至', '张', '认', '接', '告', '入', '笑', '内', '英', '军', '候', '民',
                 '岁', '往', '何', '度', '山', '觉', '路', '带', '万', '男', '边', '风', '解',
                 '叫', '任', '金', '快', '原', '吃', '妈', '变', '通', '师', '立', '象', '数',
                 '四', '失', '满', '战', '远', '格', '士', '音', '轻', '目', '条', '呢']
    # 然后把这个列表的数据与order列表数据进行一一对应打包成字典数据：键是‘正确字符名称’，值是‘正确字符最终的数据’
    font_data = dict(zip(order, font_list))
    # print(font_data)
    return cmap_dict, font_data
# 第三步==》最后再通过cmap_dict和font_dict的’正确字符的名称‘去把文章的内容中的特殊字符替换成正确的文字，并保存到本地
def get_data(res_text, cmap_dict, font_dict):
    html = etree.HTML(res_text)
    data = str(html.xpath('//div[@class="muye-reader-content noselect"]//text()'))
    # data = html.xpath('//div[@class="muye-reader-content noselect"]//text()')
    # print(type(data))
    for key, value in cmap_dict.items():  # 这里的key是特殊字符，values是正确字符的名称
        # 根据value(正确字符的名称)去font_dict里面获取对应的‘正确字符’出来
        data_value = font_dict[value]   # 这里的data_value就是按特殊字符的顺序提取的正确字符
        # 最后进行替换：
        data = data.replace(key, data_value)   # 这里的变量名必须一致才能表示在同一个结果中进行循环播放
    result = '\n'.join(eval(data.replace(r'\u', '')))
    print(result)
    with open(r'第1章_空屋.txt','w+', encoding='utf-8') as f:
        f.write(result)
text,fonturl = get_fonturl()
cmap_dict,font_data = get_font_cmap(fonturl)
get_data(text,cmap_dict,font_data)