import time,random,json,requests,sys
from lxml import etree
sys.path.append('../..')
from Error_handle import error_handing

def get_urllist_name():
    url = 'https://api.tripadvisor.cn/restapi/soa2/20874/hotelListForPc'
