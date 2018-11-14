# -*- coding: utf-8 -*-
from urllib import parse

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader

from site_crawler.items import NovelItem, NovelDjangoItem
from site_crawler.utils import get_md5, get_author_by_biquge, get_category_by_biquge


class BiqugeSpider(CrawlSpider):
    name = 'biquge'
    allowed_domains = ['www.biquge.com.tw', 'biquge.com.tw']
    start_urls = ['http://www.biquge.com.tw/']

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "ITEM_PIPELINES": {
            # 'site_crawler.pipelines.OutPutPipeline': 1,
            'site_crawler.pipelines.NovelImagePipeline': 2,
            'site_crawler.pipelines.SaveItemPipeline': 3,
        },
        "IMAGES_STORE": "/home/ouru/novels",
        "IMAGES_URLS_FIELD": "image_url",
    }

    rules = (
        Rule(LinkExtractor(allow=r'\d+_\d+/$'), callback='parse_novel', follow=True),
        Rule(LinkExtractor(allow=r'.*?/\d+.html'), callback='parse_chapter', follow=True),
    )

    def parse_novel(self, response):
        item_loader = ItemLoader(item=NovelItem(), response=response)
        item_loader.add_value("url_id", get_md5(response.url))
        item_loader.add_value("url", response.url)
        item_loader.add_css("image_url", "#fmimg img::attr(src)")
        item_loader.add_css("site_name", ".header_logo a::text")
        item_loader.add_css("novel_name", "#info h1::text")
        item_loader.add_xpath("author", "//div[@id='info']/p[1]/text()")
        item_loader.add_css("category", ".con_top::text")
        item_loader.add_css("intro", "#intro")
        item = item_loader.load_item()

        # item = NovelDjangoItem()
        # item["url_id"] = get_md5(response.url)
        # item["url"] = response.url
        # item["image_url"] = [parse.urljoin(response.url, response.css("#fmimg img::attr(src)").extract_first())]
        # item["site_name"] = response.css(".header_logo a::text").extract_first()
        # item["novel_name"] = response.css("#info h1::text").extract_first()
        #
        # author = response.xpath("//div[@id='info']/p[1]/text()").extract_first()
        # item["author"] = get_author_by_biquge(author)
        #
        # category = response.css(".con_top::text").extract()[2]
        # item["category"] = get_category_by_biquge(category)
        #
        # item["intro"] = response.css("#intro").extract_first()

        yield item

    def parse_chapter(self, response):
        i = {}
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
