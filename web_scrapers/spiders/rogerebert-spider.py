import scrapy

class RogeRebertSpider(scrapy.Spider):
    name = "rogerebertbot"
    allowed_domains = ["rogerebert.com"]

    start_urls = ["https://www.rogerebert.com/reviews"]

    def start_requests(self):
        for page_start in range(1, 850):
            yield scrapy.Request("https://www.rogerebert.com/reviews?filters%5Bgreat_movies%5D%5B%5D=&filters%5Bno_stars%5D%5B%5D=&filters%5Bno_stars%5D%5B%5D=1&filters%5Btitle%5D=&filters%5Breviewers%5D=&filters%5Bgenres%5D=&page={}&sort%5Border%5D=newest".format(page_start))

    def parse(self, response):
        hxs = scrapy.Selector(response)

        review_urls = hxs.select("//*[@id='review-list']/figure/a[@class='poster']/@href").extract()

        for url in review_urls:
            yield scrapy.Request(response.urljoin('https://www.rogerebert.com' + url), callback=self.parse_review)


    def parse_review(self, response):
        name = response.url.split('/')[-1]
        filename = '/Users/lucaverhees/IR/web_scrapers/rogerebertFiles/{}.html'.format(name)
        with open(filename, 'wb') as f:
            f.write(response.body)
            f.close()
        self.log('Saved file {}'.format(filename))


