import requests
r = requests.get("https://www.baidu.com")
# .status_code查看状态码，Response 200 说明get成功，不是200说明失败
r.status_code
r = requests.get()
# .encoding 重新编码
r.encoding = 'utf-8'
# .text 查看内容
r.text

# Requests库主要有7个主要方法，分别是：
requests.request() # 构造一个请求，支撑以下各种方法
requests.get() # 获取html网页的方法，对应于http的GET
requests.head() # 获取html网页头信息的方法，对应于http的HEAD
requests.post() # 向html网页发送POST请求的方法，对应于http的POST
requests.put() # 向html网页放松PUT请求的方法，对应于http的PUT
requests.patch() # 向html网页提交局部修改请求，对应于http的PATCH
requests.delete() # 向html网页提交删除请求，对应于http的DELETE
# 获取html网页的方法，对应于http的GET
r = requests.get(url, params=None, **kwargs) # 返回的对象是Response = 构造一个向服务器请求资源的Request对象
# url 拟获得页面的链接
# params 在url中增加的额外参数，可是字典或者字典流
# **kwargs 12个控制访问参数
type(r)
# Reture: requests.models.Response
# 在Response对象中，最常用的有以下五个属性：
r.status_code # http请求返回状态，200表示成功，404表示失败
r.text # http响应内容的字符串形式，即url对应页面的内容
r.encoding # 从http header中猜测响应内容编码方式，如果html的header中不存在charset字段，则默认编码为ISO-8859-1，这个默认编码不能识别中文
r.apparent_encoding # 从内容中分析出的响应内容编码方式。这个是根据html的body部分分析出url的编码方法
r.content # http响应内容的二进制形式

# 理解Requets库的异常
requests.ConnectionError # 网络链接异常，如DNS的查询失败，拒绝链接等
requests.HTTPError # http错误异常
requests.URLRequired # URL缺失异常
requests.TooManyRedirects # 超过最大重定向数
requests.ConnectTimeout # 链接远程服务器异常
requests.Timeout # 请求url超时
r.raise_for_status() # 如果不是200，产生异常requests.HTTPError

# 爬取网页通用框架
import requests

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"

if __name__ == "__main__":
    url = "https://www.baidu.com"
    print(getHTMLText(url))

# HTTP协议（Hypertext Transfer Protocol），超文本传输协议。
# URL格式：http://host[:port][path]
# host: 合法的Internet主机域名或者ip
# port: 端口号，缺省为80
# path: 请求资源路径
# HTTP协议对资源的操作
# GET: 请求URL位置的资源
# HEAD: 请求获取URL位置资源的响应消息报告，即获得该资源的头部信息
# POST: 请求向URL位置的资源后附加新的数据
# PUT: 请求向URL位置储存一个资源，覆盖原URL位置的资源
# PATCH: 请求局部更新URL位置资源，即改变该出处资源的部分内容
# DELETE: 请求删除URL位置储存的资源

r = requests.head(url) # 获取html网页头信息的方法，对应于http的HEAD
r.headers
r.text


payload = {'key1':'value1', 'key2':'value2'}
r = requests.post(url, data = payload) # 向html网页发送POST请求的方法，对应于http的POST
print(r.text)

requests.request(method, url, **kwargs) # 构造一个请求，支撑以下各种方法
# method 请求方式，对应get/post/put等7种
# url 拟获取页面url链接
# **kwargs 13

# 京东商品信息爬取
import requests
r = requests.get('https://item.jd.com/7651927.html')
r.status_code
r.encoding


# 登陆校园网
import requests

post_dir = 'http://10.255.248.9/portal.do?wlanuserip=10.6.57.178&wlanacname=AC3&ssid=i_sicau&mac=E8-4E-06-58-A2-B8&url=http://1.1.1.1'
post_dir = 'http://10.255.248.9/portal.do?wlanuserip=10.6.57.178&wlanacname=AC3&ssid=i_sicau&mac=E8-4E-06-58-A2-B8&url=http://1.1.1.1'
post_data = {
    'userId': '201702420',
    'passwd': '1314159Dd',
    'twiceauth': '1'
}
post_header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ca;q=0.7',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
s = requests.Session()
s.headers = post_header
s.post(post_dir, data=post_data, verify=False)



r = requests.post(post_dir, data=post_data, headers=post_header)


# 百度关键词提交
kv = {'wd':'python'}
r = requests.get("http://www.baidu.com/s", params=kv)
r.request.url # 可以查看请求的url是什么

# 爬取图片
path = "~/"
url = "http://jiaowu.sicau.edu.cn/photo/201702420.jpg"
