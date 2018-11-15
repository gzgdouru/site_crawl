# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from urllib import parse

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request

class SiteCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class OutPutPipeline(object):
    def process_item(self, item, spider):
        logger = logging.getLogger(spider.name)
        logger.info(item)
        return item


class SaveItemPipeline(object):
    def process_item(self, item, spider):
        if hasattr(item, "save_item"):
            item.save_item()
        return item


class SaveDjangoItemPipeline(object):
    def process_item(self, item, spider):
        item.save()
        return item


class NovelImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        item["image_url"] = [parse.urljoin(item["url"], image_url) for image_url in item["image_url"]]
        return [Request(x) for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        path = super(NovelImagePipeline, self).file_path(request, response, info)
        return path.replace("full/", "")

    def item_completed(self, results, item, info):
        for ok, value in results:
            if ok:
                item["image_path"] = value["path"]
            else:
                import logging
                logger = logging.getLogger(NovelImagePipeline.__name__)
                logger.error("下载图片({0})失败!".format(item["image_url"]))
        return item