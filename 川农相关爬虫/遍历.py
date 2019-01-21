import requests
from bs4 import BeautifulSoup

html = requests.get('http://jiaowu.sicau.edu.cn/web/web/web/index.asp')
html.encoding = html.apparent_encoding
soup = BeautifulSoup(html.text, features='html5lib')
for link in soup.find_all('a'):
    print(link.get_text(), link.attrs['href'])
