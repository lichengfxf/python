import requests
from pyquery import PyQuery as pq
import urllib
from os import path
import os
import re

url = "https://www.aqniu.com/"
url = "https://all.aqniu.com/"

r = requests.get(url=url)
r.encoding = "utf-8"

# 构造函数1: 使用html构造
doc = pq(r.text)
# 构造函数2: 使用url
#doc = pq(url=url, encode="utf-8")

# 创建目录
save_dir = "./imgs"
if not os.access(save_dir, os.F_OK):
    os.mkdir(save_dir)

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

#
# 爬取所有的图片
#
# 选择所有的<img>标签
images = doc('img')
#print(type(a))
#print(a)

# 遍历获取到的所有元素
for i in images.items():
    url = i.attr("src")
    us = urllib.parse.urlsplit(url)
    file_name = path.basename(us.path)
    # 'https://all.aqniu.com/wp-content/themes/HaoWa/timthumb.php?src=https://all.aqniu.com/wp-content/uploads/2021/05/137d6233b7ec79dd9e5663.jpg&h=65&w=130&zc=1'
    if not is_img_file(file_name):
        m = re.match(r'.*src=(.*?)&', url, re.I)
        img_url = m.group(1)
        us2 = urllib.parse.urlsplit(img_url)
        file_name = path.basename(us2.path)
    file_path = save_dir + "/{}".format(file_name)
    save_img(i.attr("src"), file_path)
    