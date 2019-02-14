import scrapy

class MoviewebSpider(scrapy.Spider):
    name = "movieweb"
    allowed_domains = ["movieweb.com"]

    start_urls = ["https://movieweb.com/movie-news/"]

    def start_requests(self):
        for page_start in range(1, 600):
            yield scrapy.Request("https://movieweb.com/movie-news/?page={}".format(page_start))

    def parse(self, response):
        hxs = scrapy.Selector(response)

        article_urls = hxs.select('//article/a/@href').extract()

        for url in article_urls:
            yield scrapy.Request(response.urljoin('https://movieweb.com'+url), callback=self.parse_newsarticle)


    def parse_newsarticle(self, response):
        name = response.url.split('/')[-2]
        filename = '/Users/lucaverhees/IR/ir_scraper/cinemablendFiles/{}.html'.format(name)
        with open(filename, 'wb') as f:
            f.write(response.body)
            f.close()
        self.log('Saved file {}'.format(filename))


