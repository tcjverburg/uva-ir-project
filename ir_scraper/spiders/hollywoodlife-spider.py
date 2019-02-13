from scrapy import Spider
from scrapy import Selector
from scrapy.http.request import Request
from ir_scraper.items import HollywoodlifeItem

class HollywoodlifeSpider(Spider):
    name = "hollywoodlife"
    allowed_domains = ["hollywoodlife.com"]
    start_urls = ["https://hollywoodlife.com/topics/news/"]

    def parse(self, response):
        hxs = Selector(response)

        next_page = hxs.select("//span[@class='pagination-nav__next']/a/@href").extract()

        if not not next_page:
            yield Request(next_page[0], self.parse)

        article_urls = hxs.select('//*[@id="archive-river"]/article/div[2]/div/header/h3[@class="article-feed__article-title"]/a/@href').extract()

        for url in article_urls:
            yield Request(response.urljoin(url), callback=self.parse_newsarticle)

    def parse_newsarticle(self, response):
        item = HollywoodlifeItem()
        item['title'] = response.xpath("//h1/i/text()").extract()[0]
        item['content'] = response.xpath("//h3/text()").extract()[0]
        yield item


