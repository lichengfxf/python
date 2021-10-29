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
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import json
import threading
import queue

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

#
# 后台线程: 获取视频数据
#
class get_video_thead(threading.Thread):
  def __init__(self, ID, work_queue):
    threading.Thread.__init__(self)
    self.ID = ID
    self.work_queue = work_queue

  def run(self):
    while not self.work_queue.empty():
      gv_locker.acquire()
      self.page_url, self.page_num, self.timeout = work_queue.get()
      gv_locker.release()

      #
      # 多线程环境下调用print会错乱
      #
      #print('>> [{:0>2d}]正在获取第{:0>3d}页的数据 -> {}'.format(self.ID, self.page_num, self.page_url))
      sys.stdout.write('>> [{:0>2d}]正在获取第{:0>3d}页的数据 -> {}\n'.format(self.ID, self.page_num, self.page_url))
      
      # 因为网站的大部分内容是用js动态加载的，
      # 所以必须使用webdriver访问
      browser = webdriver.Chrome()
      # 如果元素没有立即加载，最多等待多久
      browser.set_page_load_timeout(timeout)
      get_video_list(browser, self.page_url, self.timeout, self.page_num)
      browser.close()
    sys.stdout.write('>> [{:0>2d}] 线程结束...\n'.format(self.ID))


# 全局锁
gv_locker = threading.Lock()

if __name__ == '__main__':
    # 设置超时时间
    timeout = 15
    
    url = r'https://bb2240.com/guochan/p{}.html'
    
    # 初始化工作队列
    work_queue = queue.Queue(1024)    
    for i in range(1, 100):
      work_queue.put((url.format(i), i, timeout))
    
    # 初始化线程池
    gvt_list = []
    for i in range(4):
      t = get_video_thead(i, work_queue)
      t.start()
      gvt_list.append(t)

    # 等待所有线程结束
    for t in gvt_list:
      t.join()
