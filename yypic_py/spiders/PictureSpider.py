# -*- coding: utf-8 -*-
import random
import time

import scrapy

from yypic_py.items import PictureItem


class PictureSpider(scrapy.Spider):
    name = "PictureSpider"
    allowed_domains = ["www.netbian.com"]

    def __init__(self, date=None, *args, **kwargs):
        super(PictureSpider, self).__init__(*args, **kwargs)
        self.date = date
        self.start_urls = [
            "http://www.netbian.com/fengjing/",
            "http://www.netbian.com/meinv/",
            "http://www.netbian.com/rili/",
            "http://www.netbian.com/youxi/",
            "http://www.netbian.com/dongman/",
            "http://www.netbian.com/weimei/",
            "http://www.netbian.com/sheji/",
            "http://www.netbian.com/qiche/",
            "http://www.netbian.com/huahui/",
            "http://www.netbian.com/dongwu/",
            "http://www.netbian.com/renwu/",
            "http://www.netbian.com/meishi/",
            "http://www.netbian.com/shuiguo/",
            "http://www.netbian.com/jianzhu/",
            "http://www.netbian.com/yingshi/",
            "http://www.netbian.com/tiyu/",
            "http://www.netbian.com/junshi/"
        ]

    def parse(self, response):
        # time.sleep(random.randint(10, 30))  # 休眠随机时间
        # 爬取每个分类的前x页
        print("++++++++++++++++++++")
        print(self.date)
        type = response.url.split("/")[-2]
        page_urls = []
        page_urls.append(response.url)
        page_num = 6
        # 将每页的url放入数组
        # if type == 'meinv':
        #     pass

        # if type == 'fengjing':
        #     page_num = 11

        # if type == 'dongman' or type == 'youxi':
        #     page_num = 11
        # 2 11
        for page in range(2, page_num):
            page_link = response.url + 'index_' + str(page) + '.htm'
            page_urls.append(page_link)

        # 倒序，从后往前爬取
        # page_urls.reverse()
        print("===========page_urls:%s" % page_urls)

        for page_url in page_urls:
            # time.sleep(random.randint(1, 2))  # 休眠随机时间
            yield scrapy.Request(page_url, callback=self.page_pic_url)

    # 具体每一页的爬取,获取大图的链接
    def page_pic_url(self, response):
        # date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        pic_list = response.xpath('//li/a[contains(@title, "' + self.date + '")]/@href').extract()
        title_list = response.xpath('//li/a[contains(@title, "' + self.date + '")]/img/@alt').extract()
        small_pic = response.xpath('//li/a[contains(@title, "' + self.date + '")]/img/@src').extract()
        if len(pic_list) <= 0:
            date = repr(self.date).replace("-", "")[:4] + "/" + repr(self.date).replace("-", "")[4:]
            pic_list = response.xpath('//li/a/img[contains(@src, "' + date + '")]/../@href').extract()
            title_list = response.xpath('//li/a/img[contains(@src, "' + date + '")]/@alt').extract()
            small_pic = response.xpath('//li/a/img[contains(@src, "' + date + '")]/@src').extract()

        type = response.url.split('/')[-2]
        print(pic_list)
        for index in range(len(pic_list)):
            if pic_list[index] == 'http://www.netbian.com/':
                pass
            else:
                new_link = "http://www.netbian.com" + pic_list[index][:-4] + '-1920x1080.htm'
                item = PictureItem()
                item['name'] = title_list[index] + ".jpg"
                item['type'] = type
                item['small_url'] = [small_pic[index]]
                time.sleep(random.randint(1, 2))  # 休眠随机时间
                request = scrapy.Request(new_link, callback=self.pic_content)
                request.meta['item'] = item
                yield request

    def pic_content(self, response):

        real_link = response.xpath('//tr/td[contains(@align, "left")]/a/img/@src').extract()
        item = response.meta['item']
        item["img_url"] = real_link
        item["date"] = self.date
        print(item['name'])
        yield item
