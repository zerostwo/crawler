杂七杂八的爬虫脚本
===

#### 初见网络爬虫

##### BeautifulSoup

```bash
$ pip install beautifulsoup4
```

`BeautifulSoup`里有两个最常用的函数：
- `find(tag, attributes, recursive, text, limit, keywords)`
- `findAll(tag, atttibutes, recursive, text, keywords)`

其中：
- `tag`: HTML文档中的标签；
- `attributes`: 这是一个Python字典封装一个标签的若干属性和对应的属性值；
- `recursive`: 递归参数是指的摘取HTML结构中多少层信息，是个布尔变量，`True`代表所有，`False`代表第一层；
- `text`: 文本参数，根据标签内容去匹配；
- `limit`: 范围限制参数，抓取前几项，默认为1。

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