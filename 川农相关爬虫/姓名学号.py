import requests
from lxml import etree
from bs4 import BeautifulSoup
from requests import HTTPError


class SicauSpider:
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/71.0.3578.98 Safari/537.36"}

    def get_sign(self):
        index = self.session.get('http://jiaowu.sicau.edu.cn/web/web/web/index.asp', timeout=5)
        index.encoding = 'gb2312'
        seletor = etree.HTML(index.text)
        return seletor.xpath("//input[@name='sign']/@value")

    def log_sicau(self, student_id, password):
        data = {'user': student_id, 'pwd': password, 'lb': 'S', 'submit': '', 'sign': self.get_sign()}
        try:
            post_url = 'http://jiaowu.sicau.edu.cn/jiaoshi/bangong/check.asp'
            self.session.post(post_url, data=data, timeout=5, headers=self.headers)
            data = self.session.get('http://jiaowu.sicau.edu.cn/xuesheng/cx/zhcp/bzr_zhcj.asp', timeout=5)
        except HTTPError as e:
            print(e)
        data.encoding = 'gb2312'
        soup = BeautifulSoup(data.text, features='html5lib')
        for i in soup.find("table", {'class': 'tablebody'}).tr.next_siblings:
            print(i)


if __name__ == '__main__':
    student_id = '201702442'
    password = '123123'
    c = SicauSpider()
    c.log_sicau(student_id, password)
