# -*- coding: utf-8 -*-
from urllib import parse

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

from site_crawler.items import NovelItem, NovelDjangoItem, ChapterItem
from site_crawler.utils import get_md5, get_author_by_biquge, get_category_by_biquge


class BiqugeSpider(CrawlSpider):
    name = 'biquge'
    allowed_domains = ['www.biquge.com.tw', 'biquge.com.tw']
    start_urls = ['http://www.biquge.com.tw/']
    err_chapters = []

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "ITEM_PIPELINES": {
            # 'site_crawler.pipelines.OutPutPipeline': 1,
            'site_crawler.pipelines.NovelImagePipeline': 2,
            'site_crawler.pipelines.LogErrChapterPipeline': 3,
            'site_crawler.pipelines.SaveItemPipeline': 4,
            'site_crawler.pipelines.ChapterExportPipeline': 5,
        },
        "IMAGES_STORE": "/home/ouru/novels/images",
        "IMAGES_URLS_FIELD": "image_url",

        "CHAPTER_FILE_PATH": "/home/ouru/novels/chapters",
        "CHAPTER_FILE_OVERWRITE": True,
    }

    rules = (
        Rule(LinkExtractor(allow=r'\d+_\d+/$'), callback='parse_novel', follow=True),
        Rule(LinkExtractor(allow=r'.*?/\d+.html'), callback='parse_chapter', follow=True,
             process_request="custom_process_request"),
    )

    def __init__(self, *args, **kwargs):
        super(BiqugeSpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.spider_close, signals.spider_closed)

    def spider_close(self):
        self.crawler.stats.set_value("err_chapters", self.err_chapters)

    def custom_process_request(self, request):
        if request.url in self.err_chapters:
            # 章节比小说先处理的url不进行过滤
            request.dont_filter = True
        return request

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
        item_loader = ItemLoader(item=ChapterItem(), response=response)
        item_loader.add_value("url_id", get_md5(response.url))
        item_loader.add_value("url", response.url)
        item_loader.add_value("index", response.url)
        item_loader.add_css("name", ".bookname h1::text")
        item_loader.add_css("content", "#content")
        item_loader.add_xpath("novel_name", "//div[@class='con_top']/a[2]/text()")
        item = item_loader.load_item()
        return item
