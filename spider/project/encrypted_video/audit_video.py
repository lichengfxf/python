import requests
from pyquery import PyQuery as pq
import urllib
from os import path
import os
import re
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import json


url = r'https://bb2240.com/guochan/p1.html'

hearders = {'refer':url,
            'user-agent': r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36' }

# 因为网站的大部分内容是用js动态加载的，
# 所以必须使用webdriver访问
browser = webdriver.Chrome()

# 设置超时时间
timeout = 15
# 如果元素没有立即加载，最多等待多久
browser.set_page_load_timeout(timeout)

#
# 获取视频列表
#
def get_video_list(url, timeout):    
  try:
    browser.get(url=url)
  except TimeoutException:
    pass
  # 显式等待, 等到某个事件出现，或者等待超时
  wait = WebDriverWait(browser, timeout)
  video_list_locater = (By.CSS_SELECTOR, 'div.panel-max')
  wait.until(EC.visibility_of_element_located(video_list_locater))
  video_list = browser.find_elements(By.CSS_SELECTOR, 'div.panel-max > ul > li')
  for video in video_list:
    video_url = video.find_element(By.CSS_SELECTOR, 'a').get_property('href')
    video_title = video.find_element(By.CSS_SELECTOR, 'a > img').get_property('alt')
    get_video_m3u8(video_url)
    
def get_video_m3u8(url):
  r = requests.get(url)
  # cms_player = 
  m3u8_tmp = re.match(r'.*cms_player = (.*?);</script>', r.text, re.S)
  j = json.load(m3u8_tmp.group(1))
  m = j['url']
  print(m)

def main():
    get_video_list(url, timeout)  

if __name__ == '__main__':
    main()
    browser.close()