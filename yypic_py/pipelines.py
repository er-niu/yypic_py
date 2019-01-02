# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import re


class YypicPyPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # time.sleep(random.randint(1, 2))  # 休眠随机时间
        # 循环每一张图片地址下载，若传过来的不是集合则无需循环直接yield
        for image_url in item['img_url']:
            # meta里面的数据是从spider获取，然后通过meta传递给下面方法：file_path
            yield Request(image_url, meta={'name': item['name'], 'type': item['type'], 'small': 0, 'date': item['date']})

        # for small_url in item['small_url']:
        # meta里面的数据是从spider获取，然后通过meta传递给下面方法：file_path
        # yield Request(small_url, meta={'name': item['name'], 'type': item['type'], 'small': 1})

    def file_path(self, request, response=None, info=None):
        # 接收上面meta传递过来的图片名称
        name = request.meta['name']
        type = request.meta['type']
        date = request.meta['date']
        # date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # 过滤windows字符串，不经过这么一个步骤，你会发现有乱码或无法下载
        name = re.sub(r'[？\\*|“<>:/]', '', name)
        if request.meta['small'] == 1:
            filename = u'{0}/{1}/{2}'.format(type, "/small/", name)
        else:
            # 分文件夹存储的关键：{0}对应着type；{1}对应着name
            filename = u'{0}/{1}/{2}'.format(type, date, name)
        return filename
