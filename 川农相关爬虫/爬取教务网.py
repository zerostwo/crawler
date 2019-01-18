import requests
import re
from lxml import etree
import prettytable as pt


def log_scau(id, pwd):
    # 本代码共分为2部分
    session = requests.Session() # 创建会话连接，好处是会自动提交cookie，大大节省精力和代码量
    index = session.get('http://jiaowu.sicau.edu.cn/web/web/web/index.asp', timeout=5)
    # 第一部分，准备post提交的数据
    index.encoding = 'gb2312'
    seletor=etree.HTML(index.text)
    sign = seletor.xpath("//input[@name='sign']/@value")       # 利用xpath找到sign的值

    data = {                                          # 需要提交的数据
        'user': id,
        'pwd': pwd,
        'lb': 'S',
        'submit': '',
        'sign': sign
    }
    # 第二部分，尝试登陆
    try:
        post_url = 'http://jiaowu.sicau.edu.cn/jiaoshi/bangong/check.asp'  # 验证密码的网站
        session.post(post_url, data=data, timeout=5) # 先登陆验证密码网站
        data = session.get('http://jiaowu.sicau.edu.cn/xuesheng/bangong/main/index1.asp', timeout=5)  # 跳转到个人主页
        kao = session.get('http://jiaowu.sicau.edu.cn/xuesheng/kao/kao/xuesheng.asp', timeout=5)
        info = session.get('http://jiaowu.sicau.edu.cn/xuesheng/dangan/banji/bjiben.asp', timeout=5)
        data.encoding = 'gb2312'
        kao.encoding = 'gb2312'
        # name = re.compile('<td width="99" align="left">(.*)</td>').findall(data.text)  # 正则匹配你的名字
        # 考试安排
        course = re.compile('<td width=200>(.*)&nbsp; </td>').findall(kao.text)
        time = re.compile('<td width=320>(.*) </td>').findall(kao.text)
        location = re.compile('<td width=130>(.*)&nbsp; </td>').findall(kao.text)
        number = re.compile('<td width=50>(.*)&nbsp; </td>').findall(kao.text)
        tb = pt.PrettyTable()
        tb.add_column('课程', course)
        tb.add_column('时间', time)
        tb.add_column('地点', location)
        tb.add_column('座位号', number)
        tb.set_style(pt.DEFAULT)
        print(tb)
        # 个人信息

    except:
        print('密码错误')

id = '201702420'
pwd = '981211'
log_scau(id, pwd)
