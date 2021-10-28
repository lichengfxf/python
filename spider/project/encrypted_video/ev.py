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
import time

url = r'https://www.hxcpp73.com/videoContent/27164'

hearders = {'refer':r'https://www.hxcpp73.com/?id=22929',
            'user-agent': r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36' }

# 因为网站的大部分内容是用js动态加载的，
# 所以必须使用webdriver访问
browser = webdriver.Chrome()

# 设置超时时间
timeout = 10
# 如果元素没有立即加载，最多等待多久
browser.implicitly_wait(timeout)
browser.get(url=url)

# 显式等待, 等到某个事件出现，或者等待超时
# 可以等待的事件如下
'''
title_is:判断当前页面的title是否完全等于（==）预期字符串，返回是布尔值
title_contains 判断当前页面的title是否包含预期字符串，返回布尔值
presence_of_element_located:判断某个元素是否被加到了dom树里，并不代表该元素一定可见
visibility_of_element_located : 判断某个元素是否可见. 可见代表元素非隐藏，并且元素的宽和高都不等于0
visibility_of :跟上面的方法做一样的事情，只是上面的方法要传入locator，这个方法直接传定位到的element就好了
presence_of_all_elements_located : 判断是否至少有1个元素存在于dom树中。举个例子，如果页面上有n个元素的class都是'column-md-3'，那么只要有1个元素存在，这个方法就返回True
text_to_be_present_in_element : 判断某个元素中的text是否 包含 了预期的字符串
text_to_be_present_in_element_value:判断某个元素中的value属性是否 包含 了预期的字符串
frame_to_be_available_and_switch_to_it : 判断该frame是否可以switch进去，如果可以的话，返回True并且switch进去，否则返回False
invisibility_of_element_located : 判断某个元素中是否不存在于dom树或不可见
staleness_of :等某个元素从dom树中移除，注意，这个方法也是返回True或False
element_to_be_clickable : 判断某个元素中是否可见并且是enable的，这样的话才叫clickable
element_to_be_selected:判断某个元素是否被选中了,一般用在下拉列表
element_selection_state_to_be:判断某个元素的选中状态是否符合预期
element_located_selection_state_to_be:跟上面的方法作用一样，只是上面的方法传入定位到的element，而这个方法传入locator
alert_is_present : 判断页面上是否存在alert
'''
wait = WebDriverWait(browser, timeout)

# 等待播放按钮出现，并且点击播放
btn_video_play_locater = (By.CLASS_NAME, 'el-icon-video-play')
btn_video_play = wait.until(EC.element_to_be_clickable(btn_video_play_locater))
btn_video_play.click()

# 获取视频地址
'''
  response = requests.request("GET", url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    videoId = soup.find_all('video', class_="video-js")[0]['data-video-id'] ##获取视频Id
    title = soup.find_all('h1', class_="video-player__title")[0].contents[0] ##获取视频标题
    url = "https://secure.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId={}&secure=true".format(videoId)  ##生成视频下载Url
    filename = '{}.mp4'.format(title).replace(" ","-")
    cmd_str = 'ffmpeg -i \"' + url + '\" ' + '-acodec copy -vcodec copy -absf aac_adtstoasc ' + pwd + "/" +filename  ##下载视频
    print(cmd_str)
    subprocess.call(cmd_str,shell=True)
'''

time.sleep(10000)
browser.close()
