from typing import Any
import logging
import scrapy
from scrapy.http import Response




class SoftoSpider(scrapy.Spider):
    name = "softo_spider"
    start_urls = ['https://softo.ag3nts.org']


    def parse(self, response: Response, **kwargs: Any) -> Any:
        text = response.xpath('//body').getall()
        clean_text = " ".join([t.strip() for t in text if t.strip()])
        yield {"text": clean_text}
        links = response.css("a::attr(href)").getall()
        for link in links:
            if "czescizamienne" in link or "loop" in link:
                continue
            yield response.follow(url=link, callback=self.parse)


