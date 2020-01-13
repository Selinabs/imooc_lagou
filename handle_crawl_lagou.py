# _*_ coding : UTF-8 _*_
# 开发人员："夏沫丶"
# 开发时间： 2019/11/13 20:34
# 文件名称： handle_crawl_lagou.py
# 开发工具： PyCharm
import json
import re
import time
import multiprocessing
import requests
from handle_insert_data import lagou_mysql
import xlsxwriter


class HandleLaGou(object):
    def __init__(self):
        # 使用session保存cookies信息
        self.lagou_session = requests.session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        }
        self.city_list = " "

    # 定义获取全国城市列表的方法
    def handle_city(self):
        city_search = re.compile(r'zhaopin/">(.*?)</a>')
        city_url = "https://www.lagou.com/jobs/allCity.html"
        city_result = self.handle_request(method="GET", url=city_url)
        # print(city_result)
        self.city_list = city_search.findall(city_result)
        self.lagou_session.cookies.clear()
        print(self.city_list)

    def handle_city_job(self, city):
        first_request_url = "https://www.lagou.com/jobs/list_Python?&city=%s&cl=false&fromSearch=true&labelWords=&suginput=" % city
        first_reponse = self.handle_request(method="GET", url=first_request_url)
        total_page_search = re.compile(r'class="span\stotalNum">(\d+)</span>')
        try:
            total_page = total_page_search.search(first_reponse).group(1)
        except:
            return
        else:
            for i in range(1, int(total_page) + 1):
                data = {
                    "pn": i,
                    "kd": "python"
                }
                page_url = "https://www.lagou.com/jobs/positionAjax.json?city=%s&needAddtionalResult=false" % city
                referer_url = "https://www.lagou.com/jobs/list_Python?city=%s&cl=false&fromSearch=true&labelWords=&suginput=" % city
                self.headers['Referer'] = referer_url.encode()
                response = self.handle_request(method="POST", url=page_url, data=data, info=city)
                # print(response)
                lagou_data = json.loads(response)
                job_list = lagou_data['content']['positionResult']['result']
                for job in job_list:
                    lagou_mysql.insert_item(job)

    def handle_request(self, method, url, data=None, info=None):
        while True:
            # 加入代理
            proxyinfo = "http://%s:%s@%s:%s" % ('HP22Y582B5RP159D', '447C921A6443EF79', 'http-dyn.abuyun.com', '9020')
            proxy = {
                "http": proxyinfo,
                "https": proxyinfo
            }
            try:
                if method == "GET":
                    response = self.lagou_session.get(url=url, headers=self.headers, proxies=proxy, timeout=6)
                elif method == "POST":
                    response = self.lagou_session.post(url=url, headers=self.headers, data=data, proxies=proxy, timeout=6)
            except:
                # 先清除cookies，再从新请求
                self.lagou_session.cookies.clear()
                first_request_url = "https://www.lagou.com/jobs/list_Python?&px=default&city=%s" % info
                first_reponse = self.handle_request(method="GET", url=first_request_url)
                time.sleep(10)
                continue
            response.encoding = "utf-8"
            if '频繁' in response.text:
                print(response.text)
                # 先清除cookies，再从新请求
                self.lagou_session.cookies.clear()
                first_request_url = "https://www.lagou.com/jobs/list_Python?&px=default&city=%s" % info
                first_reponse = self.handle_request(method="GET", url=first_request_url)
                time.sleep(10)
                continue
            return response.text


if __name__ == "__main__":
    lagou = HandleLaGou()
    lagou.handle_city()
    pool = multiprocessing.Pool(2)
    for city in lagou.city_list:
        pool.apply_async(lagou.handle_city_job, args=(city,))
    pool.close()
    pool.join()
