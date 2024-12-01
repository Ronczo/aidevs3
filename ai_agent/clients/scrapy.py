
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
from spiders.softo import SoftoSpider
from scrapy import signals

class ScrapyClient:
    spiders = {SoftoSpider.name: SoftoSpider}

    def __init__(self):
        self.results = []
    def run_spider(self, spider_name: str):
        spider = self.spiders.get(spider_name)
        if spider is None:
            raise ValueError(f"Spider {spider_name} not found")

        settings = get_project_settings()
        settings.set('LOG_LEVEL', 'DEBUG')  # Ustawiamy poziom logowania na DEBUG
        settings.set('LOG_FILE', 'scrapy_log.txt')  # Logowanie do pliku
        process = CrawlerProcess(settings)
        process.crawl(spider)
        dispatcher.connect(self.store_results, signal=signals.item_scraped)
        process.start()


    def store_results(self, item, spider):
        self.results.append(item)