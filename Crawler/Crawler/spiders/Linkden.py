import scrapy

from scrapy.http import FormRequest

class LoginSpider(scrapy.Spider):
    name = 'login'
    start_urls = ['https://www.linkedin.com/uas/login']

    def parse(self,response):
        self.logger.info("HI pls work")
        csrf_token = response.css("input::attr('value')").getall()
        print(csrf_token)
        formdata = {
            "csrfToken":csrf_token[0],
            "session_key":"as7122000@gmail.com",
            "ac":csrf_token[1],
            "sIdString":csrf_token[2],
            "parentPageKey":csrf_token[3],
            "pageInstance":csrf_token[4],
            "trk": "guest_homepage-basic_nav-header-signin",
            "authUUID":"",
            "session_redirect":"",
            "loginCsrfParam":csrf_token[8],
            "fp_data":csrf_token[9],
            "apfc":csrf_token[10],
            "_d":csrf_token[11],
            "showGoogleOneTapLogin":csrf_token[12],
            "controlId":csrf_token[13],
            "session_password":"!Abhi987",
            "loginFlow":"REMEMBER_ME_OPTIN"
        }
        print(formdata)
        FormRequest.from_response(response, formdata=formdata, callback=self.parse)
        yield FormRequest.from_response(response, formdata=formdata, callback=self.parse)

    def parse_after_login(self,response):
        print("Inside this now")