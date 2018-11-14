# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity
from scrapy_djangoitem import DjangoItem

from site_crawler.utils import get_category_by_biquge, get_author_by_biquge
from repo.models import Novel, NovelCategory, NovelAuthor


class SiteCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class NovelItem(scrapy.Item):
    url_id = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    image_url = scrapy.Field()
    image_path = scrapy.Field()
    site_name = scrapy.Field(output_processor=TakeFirst())
    novel_name = scrapy.Field(output_processor=TakeFirst())
    author = scrapy.Field(input_processor=MapCompose(get_author_by_biquge), output_processor=TakeFirst())
    category = scrapy.Field(input_processor=MapCompose(get_category_by_biquge), output_processor=Join(""))
    intro = scrapy.Field(output_processor=TakeFirst())

    def save_item(self):
        if not Novel.objects.filter(novel_name=self["novel_name"]).exists():
            novel = Novel()
            novel.url_id = self["url_id"]
            novel.url = self["url"]
            novel.image_url = ",".join(self["image_url"])
            novel.image_path = self["image_path"]
            novel.site_name = self["site_name"]
            novel.novel_name = self["novel_name"]

            author = NovelAuthor.objects.filter(name=self["author"]).first()
            if not author:
                author = NovelAuthor(name=self["author"])
                author.save()
            novel.author = author

            category = NovelCategory.objects.filter(name=self["category"]).first()
            if not category:
                category = NovelCategory(name=self["category"])
                category.save()
            novel.category = category

            novel.intro = self["intro"]
            novel.save()


class NovelDjangoItem(DjangoItem):
    django_model = Novel
