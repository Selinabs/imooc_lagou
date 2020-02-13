# _*_ coding : UTF-8 _*_
# 开发人员："夏沫丶"
# 开发时间： 2020/2/12 22:48
# 文件名称： test.py
# 开发工具： PyCharm
import requests

url = "https://movie.douban.com/top250"
responese = requests.get(url)
print(responese.text)
#没有返回数据可能是headers
