#
# requests库的基本用法
#

import requests

# 请求url
r = requests.get("https://www.baidu.com")

# 服务器返回的原始内容
print(type(r.content))
print(r.content)
with open("baidu_content.html", "wb") as f:
    f.write(r.content)

# 将服务器返回的内容转成文本
r.encoding = 'utf-8'
print(type(r.text))
print(r.text)
# 默认编码保存, 测试下来发现是gb2312编码保存的
with open("baidu_text_wt.html", "wt") as f:
    f.write(r.text)
# utf-8编码保存
with open("baidu_text_wb.html", "wb") as f:
    f.write(r.text.encode('utf-8'))
