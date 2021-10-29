import requests
from pyquery import PyQuery as pq
import urllib
from os import path
import os
import sys
import re
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.common.exceptions import TimeoutException
import time
import json
import threading
import queue
from concurrent.futures import ThreadPoolExecutor
from concurrent import futures

#
# 请求页面，处理异常
#
def get_page(url, timeout):
  try:
    r = requests.get(url=url, timeout=timeout)
    if r.ok:
      r.encoding = 'utf-8'
      return r.text
    else:
      return ''
  except requests.RequestException:
    return ''
#
# 获取视频列表
#
def get_video_list(browser, url, timeout, page_num):
  print(">> 开始解析网页{}".format(url))
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
    video_m3u8_url = get_video_m3u8(browser, video_url, timeout)
    if len(video_m3u8_url) == 0:
      print('获取video_m3u8_url失败')
    else:
      print(">> 正在从第{}页获取视频: {} -> {}".format(page_num, video_title, video_m3u8_url))
      cmd = r'ffplay -y 800 -i "{}"'.format(video_m3u8_url)
      # 创建目录并保存
      dir = r'video/{}/'.format(page_num)
      if not os.access(dir, os.F_OK):
        os.makedirs(dir)
      with open(dir + video_title + '.m3u8.bat', 'wb') as f:
        f.write(cmd.encode('utf-8'))

#
# 从播放页面中获取m3u8视频地址
#
def get_video_m3u8(browser, url, timeout):
  html = get_page(url, timeout)
  if len(html) == 0:
    return ''
  m3u8_tmp = re.match(r'.*cms_player = (.*?);</script>', html, re.S)
  j = json.loads(m3u8_tmp.group(1))
  url_m3 = j['url']
  html = get_page(url_m3, timeout)
  if len(html) == 0:
    return ''
  # 拼接完整地址 /20211022/ZNjFC7l5/800kb/hls/index.m3u8
  file_path = re.search(r'/.*index\.m3u8', html, re.S).group()
  return "https://vip5.bobolj.com" + file_path

# 使用selenium获取视频
def do_get_video_list(page_url, page_num, timeout):  
  # 多线程环境下调用print会错乱
  sys.stdout.write('>> [{}] 正在获取第{:0>3d}页的数据 -> {}\n'.format(threading.current_thread().name, page_num, page_url))
  
  # 因为网站的大部分内容是用js动态加载的，
  # 所以必须使用webdriver访问
  browser = webdriver.Chrome()
  # 如果元素没有立即加载，最多等待多久
  browser.set_page_load_timeout(timeout)
  get_video_list(browser, page_url, timeout, page_num)
  browser.close()
  time.sleep(1)

if __name__ == '__main__':
    # 设置超时时间
    timeout = 15
    
    url = r'https://bb2240.com/guochan/p{}.html'
    
    #
    # 线程池 concurrent 和 threading 库相比
    # 1. 使用线程池的优点是代码简单
    # 2. 缺点是没法控制线程内部执行的动作
    #    例如threading中可以4个线程, 每个线程打开一个browser, 从队列中获取任务url调用get获取页面, 只需要打开4个浏览器
    #    使用concurrent则需要每个任务都创建一个browser用完之后再关闭, 所有操作都只能封装在一个函数里, 当然也可以先创建几个browser对象, 通过参数传入
    # 3. 如果不考虑性能, 使用concurrent更方便
    with ThreadPoolExecutor(max_workers=4) as pool:
      tasks = []
      for i in range(1, 100):
        t = pool.submit(do_get_video_list, url.format(i), i, timeout)
        tasks.append(t)

      # 等待所有任务结束
      #wait(tasks)

      # 单独等待每一个任务结束
      for f in futures.as_completed(tasks):
        print(f)
      
