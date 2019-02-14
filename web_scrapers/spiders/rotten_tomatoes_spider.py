import scrapy
import json

class rotten_tomatoes(scrapy.Spider):
    name = 'tomato_scroll'
    api_url = 'https://www.rottentomatoes.com/api/private/v2.0/browse?maxTomato=100&maxPopcorn=100&services=amazon%3Bhbo_go%3Bitunes%3Bnetflix_iw%3Bvudu%3Bamazon_prime%3Bfandango_now&certified&sortBy=release&type=dvd-streaming-all&page={}'
    page = 1
    start_urls = [api_url.format(page)]

    def parse(self, response):
        data = json.loads(response.text)
        for result in data['results']:
                yield {
                    'id': result['id'],
                    'title': result['title'],
                    'url': result['url'],
                    'score': result['tomatoScore']
            }

        if data['counts']['total'] - data['counts']['count'] > 0:
            self.page += 1
            yield scrapy.Request(url=self.api_url.format(self.page), callback = self.parse)


