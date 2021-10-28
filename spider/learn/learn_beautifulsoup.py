import requests
from pyquery import PyQuery as pq
import urllib
from os import path
import os
import re
from bs4 import BeautifulSoup as bs

url = r'https://www.baidu.com'

hearders = {'user-agent': r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36' }

# 发起请求
r = requests.get(url=url, headers=hearders)
r.encoding = 'utf-8'
print(r.text)

# 格式化输出
soup = bs(r.text, 'lxml')
print(soup.prettify())
