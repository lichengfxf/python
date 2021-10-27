import requests

r = requests.get("https://www.baidu.com")
type(r.content)
print(r.content)

r.encoding = 'utf-8'
type(r.text)
print(r.text)
