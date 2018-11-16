# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from urllib import parse
import os

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem

from site_crawler.items import ChapterItem
from repo.models import Novel


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
        if "image_url" in item:
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
                print("下载图片({0})失败!".format(item["image_url"]))
        return item


class ChapterExportPipeline(object):
    def __init__(self, crawler):
        self.savePath = crawler.settings.get("CHAPTER_FILE_PATH", "novels/chapters/")
        self.overwrite = crawler.settings.get("CHAPTER_FILE_OVERWRITE", False)

    def process_item(self, item, spider):
        if isinstance(item, ChapterItem):
            savePath = os.path.join(self.savePath, item["url_id"])
            if not os.path.exists(savePath):
                os.makedirs(savePath)

            file = os.path.join(savePath, "{0}.txt".format(item["index"]))
            is_exists = os.path.exists(file)
            if (is_exists and self.overwrite) or not is_exists:
                with open(file, "w+", encoding="utf-8") as f:
                    f.write(item["content"])
        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)


class LogErrChapterPipeline(object):
    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_item(self, item, spider):
        if isinstance(item, ChapterItem) and not Novel.objects.filter(novel_name=item["novel_name"]).exists():
            #记录章节比小说先处理的记录
            spider.err_chapters.append(item["url"])
            raise DropItem("chapter({0}) error!".format(item["name"]))
        return item
