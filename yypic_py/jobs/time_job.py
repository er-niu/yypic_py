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
    # 定时任务
    # 1. 根据当前日期爬取最新图片，并保存到/分类/日期/ 文件夹 2016-07-23
    # 2. 读取文件夹图片，保存到fastfds和mysql scrapy crawl PictureSpider -a date="2019-01-09"
    # date = '2019-01-08'
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

sched = BlockingScheduler()
# 定时每天 xx:xx 执行任务
sched.add_job(my_job, 'cron', day_of_week='0-6', hour=read_conf.get_conf('job', 'hour'),
              minute=read_conf.get_conf('job', 'minute'), second=read_conf.get_conf('job', 'second'),
              end_date='2114-05-30')

sched.start()
