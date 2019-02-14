import scrapy

class HollywoodlifeSpider(scrapy.Spider):
    name = "hollywoodlifebot"
    allowed_domains = ["hollywoodlife.com"]

    start_urls = ["https://hollywoodlife.com/topics/news/"]

    def parse(self, response):
        hxs = scrapy.Selector(response)

        next_page = hxs.select("//span[@class='pagination-nav__next']/a/@href").extract()

        if not not next_page:
            yield scrapy.Request(next_page[0], self.parse)

        article_urls = hxs.select('//*[@id="archive-river"]/article/div[2]/div/header/h3[@class="article-feed__article-title"]/a/@href').extract()

        for url in article_urls:
            yield scrapy.Request(response.urljoin(url), callback=self.parse_newsarticle)


    def parse_newsarticle(self, response):
        name = response.url.split('/')[-2]
        filename = '/Users/lucaverhees/IR/web_scrapers/hollywoodlifeFiles/{}.html'.format(name)
        with open(filename, 'wb') as f:
            f.write(response.body)
            f.close()
        self.log('Saved file {}'.format(filename))


