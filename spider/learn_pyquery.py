import requests
from pyquery import PyQuery as pq
import urllib
from os import path
import re

url = "https://www.aqniu.com/"
url = "https://all.aqniu.com/"

r = requests.get(url=url)
r.encoding = "utf-8"

# 构造函数1: 使用html构造
doc = pq(r.text)
# 构造函数2: 使用url
#doc = pq(url=url, encode="utf-8")

# 选择所有的<a>标签
a = doc('img')
#print(type(a))
#print(a)

# 保存url中的图片到文件
def save_img(url, file):
    r = requests.get(url)
    with open(file, "wb") as f:
        f.write(r.content)

def is_img_file(file):
    if file.lower().endswith(('.svg', '.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
        return True
    else:
        return False

# 遍历获取到的所有元素
for i in a.items():
    url = i.attr("src")
    us = urllib.parse.urlsplit(url)
    file_name = path.basename(us.path)
    # 'https://all.aqniu.com/wp-content/themes/HaoWa/timthumb.php?src=https://all.aqniu.com/wp-content/uploads/2021/05/137d6233b7ec79dd9e5663.jpg&h=65&w=130&zc=1'
    if not is_img_file(file_name):
        m = re.match(r'.*src=(.*?)&', url, re.I)
        img_url = m.group(1)
        us2 = urllib.parse.urlsplit(img_url)
        file_name = path.basename(us2.path)
    file_path = "./img/{}".format(file_name)
    save_img(i.attr("src"), file_path)
    # 获取属性
    #print(i.attr('href'))
