# _*_ coding : UTF-8 _*_
# 开发人员："夏沫丶"
# 开发时间： 2019/11/14 23:09
# 文件名称： create_lagou_tables.py
# 开发工具： PyCharm
from sqlalchemy import create_engine, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column

engine = create_engine("mysql+pymysql://user:password@service:port/lagou?charset=utf8")

Session = sessionmaker(bind=engine)

Base = declarative_base()


class Lagoutables(Base):
    __tablename__ = 'lagou_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    positionID = Column(Integer, nullable=True)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    positionName = Column(String(length=50), nullable=False)
    workYear = Column(String(length=20), nullable=False)
    education = Column(String(length=20), nullable=False)
    jobNature = Column(String(length=20), nullable=True)
    financeStage = Column(String(length=30), nullable=True)
    companySize = Column(String(length=30), nullable=True)
    industryField = Column(String(length=30), nullable=True)
    city = Column(String(length=50), nullable=False)
    positionAdvantage = Column(String(length=200), nullable=True)
    companyShortName = Column(String(length=50), nullable=True)
    companyFullName = Column(String(length=200), nullable=True)
    district = Column(String(length=20), nullable=True)
    companyLabelList = Column(String(length=200), nullable=True)
    salary = Column(String(length=20), nullable=False)
    crawl_date = Column(String(length=20), nullable=False)


if __name__ == "__main__":
    Lagoutables.metadata.create_all(engine)
