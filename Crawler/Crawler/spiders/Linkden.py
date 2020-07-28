import scrapy

from scrapy.http import FormRequest

class LoginSpider(scrapy.Spider):
    name = 'login'
    start_urls = ['https://www.linkedin.com/uas/login']

    def parse(self,response):
        self.logger.info("HI pls work")
        csrf_token = response.css("input::attr('value')").getall()
        print("csrf",csrf_token)
        yield csrf_token
        #yield FormRequests.from_response(response, formdata={'csrf_token': csrf_token, 'user':'user', 'pass','pass'}, callback=self.parse_after_login)

    def parse_after_login(self,response):
        pass