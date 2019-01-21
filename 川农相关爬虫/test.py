import requests
from lxml import etree
from bs4 import BeautifulSoup
from requests import HTTPError

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/71.0.3578.98 Safari/537.36"}


def get_sign():
    index = session.get('http://jiaowu.sicau.edu.cn/web/web/web/index.asp', timeout=5)
    index.encoding = 'gb2312'
    seletor = etree.HTML(index.text)
    return seletor.xpath("//input[@name='sign']/@value")


def log_sicau(student_id, password):
    data = {'user': student_id, 'pwd': password, 'lb': 'S', 'submit': '', 'sign': get_sign()}
    try:
        post_url = 'http://jiaowu.sicau.edu.cn/jiaoshi/bangong/check.asp'
        session.post(post_url, data=data, timeout=5, headers=headers)
        data = session.get('http://jiaowu.sicau.edu.cn/xuesheng/bangong/main/index1.asp', timeout=5)
    except HTTPError as e:
        print(e)
    data.encoding = 'gb2312'
    soup = BeautifulSoup(data.text, features='html5lib')
    info = soup.find_all('font', {"color": "#339999"})
    for i in info:
        print(i.string)


if __name__ == '__main__':
    student_id = '201708490'
    password = '123456'
    log_sicau(student_id, password)
