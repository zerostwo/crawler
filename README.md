杂七杂八的爬虫脚本
===

#### 初见网络爬虫

##### 安装BeatifulSoup

```bash
$ pip install beatifulsoup4
```

##### 可靠的网络连接

网络异常表现为两种：
- 网页服务器上不存在
当发生异常时， 程序会抛出`HTTP`错误，可能是`404 Page Not Found` 或者 `500 Internal Server Error`等；
可以使用以下方式处理这种问题:

```python
from requests import HTTPError, get
try:
    html = get("https://zerostwo.github.io")
except HTTPError as e:
    print(e)
else:
    pass
```

- 服务器不存在
如果服务器不存在，程序将会返回`None`。

```python
from requests import get
html = get("https://zerostwo.github.io")
if html is None:
    print("URL is not found")
else:
    pass
```