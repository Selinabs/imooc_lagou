# _*_ coding : UTF-8 _*_
# 开发人员："夏沫丶"
# 开发时间： 2019/11/20 19:54
# 文件名称： handle_insert_data.py
# 开发工具： PyCharm
from lagou_spider.create_lagou_tables import Lagoutables
from lagou_spider.create_lagou_tables import Session
import time


class HandleLagouData(object):
    def __init__(self):
        self.mysql_session = Session()
        self.date = time.strftime("%Y-%m-%d", time.localtime())

    def insert_item(self, item):
        date = time.strftime("%Y-%m-%d", time.localtime())
        data = Lagoutables(
            positionID=item['positionId'],
            longitude=item['longitude'],
            latitude=item['latitude'],
            positionName=item['positionName'],
            workYear=item['workYear'],
            education=item['education'],
            jobNature=item['jobNature'],
            financeStage=item['financeStage'],
            companySize=item['companySize'],
            industryField=item['industryField'],
            city=item['city'],
            positionAdvantage=item['positionAdvantage'],
            companyShortName=item['companyShortName'],
            companyFullName=item['companyFullName'],
            district=item['district'],
            companyLabelList=','.join(item['companyLabelList']),
            salary=item['salary'],
            crawl_date=date
        )
        query_result = self.mysql_session.query(Lagoutables).filter(Lagoutables.crawl_date == date,
                                                                    Lagoutables.positionID == item[
                                                                        "positionId"]).first()
        if query_result:
            print("该岗位信息已存在%s:%s:%s" % (item["positionId"], item["city"], item["positionName"]))
        else:
            self.mysql_session.add(data)
            self.mysql_session.commit()
            print("新增岗位信息%s" % item["positionId"])

    def
lagou_mysql = HandleLagouData()