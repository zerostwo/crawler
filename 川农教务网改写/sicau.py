import requests
from lxml import etree
from bs4 import BeautifulSoup
from requests import HTTPError


class ExaminationArrangement:
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/71.0.3578.98 Safari/537.36"}

    def get_sign(self):
        index = self.session.get('http://jiaowu.sicau.edu.cn/web/web/web/index.asp', timeout=5)
        index.encoding = 'gb2312'
        return etree.HTML(index.text).xpath("//input[@name='sign']/@value")

    def inquire(self, student_id, password):
        data = {'user': student_id, 'pwd': password, 'lb': 'S', 'submit': '', 'sign': self.get_sign()}
        try:
            post_url = 'http://jiaowu.sicau.edu.cn/jiaoshi/bangong/check.asp'
            self.session.post(post_url, data=data, timeout=5, headers=self.headers)
            data = self.session.get('http://jiaowu.sicau.edu.cn/xuesheng/kao/kao/xuesheng.asp', timeout=5)
        except HTTPError as e:
            print(e)
        data.encoding = 'gb2312'
        soup = BeautifulSoup(data.text, features='html5lib')
        subject = soup.find_all('td', {"width": "200"})
        time = soup.find_all('td', {"width": "320"})[1:]
        classroom = soup.find_all('td', {"width": "130"})[1:]
        method = soup.find_all('td', {"width": "80"})[2:]
        seat_number = soup.find_all('td', {"width": "50"})
        seat_number = seat_number[2:]
        examination_arrangement = []
        for i in range(len(subject)):
            intermediate = {
                'num': seat_number[i * 2].string,
                'subject': subject[i].string.strip(),
                'time': time[i].string,
                'classroom': classroom[i].string.strip(),
                'method': method[i].string.strip(),
                'seat_num': seat_number[i * 2 - 1].string.strip()}
            examination_arrangement.append(intermediate)
        return examination_arrangement
