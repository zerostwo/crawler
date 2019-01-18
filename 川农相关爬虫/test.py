import requests
import re
from lxml import etree
from bs4 import BeautifulSoup
import prettytable as pt

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/71.0.3578.98 Safari/537.36"}


def get_sign():
    index = session.get('http://jiaowu.sicau.edu.cn/web/web/web/index.asp', timeout=5)
    index.encoding = 'gb2312'
    seletor = etree.HTML(index.text)
    return seletor.xpath("//input[@name='sign']/@value")


def log_sicau(id, pwd):
    data = {
        'user': id,
        'pwd': pwd,
        'lb': 'S',
        'submit': '',
        'sign': get_sign()
    }
    try:
        post_url = 'http://jiaowu.sicau.edu.cn/jiaoshi/bangong/check.asp'
        session.post(post_url, data=data, timeout=5, headers=headers)
        data = session.get('http://jiaowu.sicau.edu.cn/xuesheng/bangong/main/index1.asp', timeout=5)
        data.encoding = 'gb2312'

    except:
        print('密码错误')


id = '201702420'
pwd = '981211'
log_sicau(id, pwd)
