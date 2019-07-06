# -*- coding:utf-8 -*-
import os
import subprocess
import time

from apscheduler.schedulers.blocking import BlockingScheduler

import logging

from yypic_py.conf import read_conf
from yypic_py.service import scan_upload_day

logging.basicConfig()


def my_job():
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    # date = '2019-06-26'
    # 定时任务
    # 1. 根据当前日期爬取最新图片，并保存到/分类/日期/ 文件夹 2016-07-23
    # 2. 读取文件夹图片，保存到fastfds和mysql scrapy crawl PictureSpider -a date="2019-01-09"
    # date = '2019-06-10'
    # dates = {"2019-01-08", "2019-01-09", "2019-01-10"}
    # for date in dates:
    #     p = subprocess.Popen("scrapy crawl PictureSpider -a date=" + date + "", shell=True, stdout=subprocess.PIPE)
    #
    #     print("the scrapy excute...: %s", time.localtime(time.time()))
    #     p.wait()
    #     print("waiting ...the scrapy excute done: %s", time.localtime(time.time()))
    #
    #     scan_upload_day.upload_pic(date)

    p = subprocess.Popen("scrapy crawl PictureSpider -a date=" + date + "", shell=True, stdout=subprocess.PIPE)
    print("the scrapy excute...: %s", time.localtime(time.time()))
    p.wait()
    print("waiting ...the scrapy excute done: %s", time.localtime(time.time()))
    scan_upload_day.upload_pic(date)
