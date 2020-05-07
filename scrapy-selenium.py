import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.webdriver.common.keys import Keys
import time


class SS01Spider(scrapy.Spider):
    name = 'ss01'
    contador=0
    def start_requests(self):
        yield SeleniumRequest(
            url="https://finance.yahoo.com/screener/unsaved/8a966db8-4b7d-47e3-bdfb-36067d206e11?offset=0&count=100",
            wait_time=7,
            callback=self.parse_0,
            script='window.scrollTo(0, document.body.scrollHeight);')


    def parse_0(self, response):        # sinsce we dint modify nothing we can use response method directly
        links = response.xpath('//td[@aria-label="Symbol"]/a')
        for link in links[10:]:
            SS01Spider.contador+=1
            time.sleep(2)
            stock_link = "https://finance.yahoo.com"+link.xpath('.//@href').get()
            print(stock_link)

            if SS01Spider.contador < 4:
                yield SeleniumRequest(
                    url=stock_link,
                    wait_time=20,
                    screenshot=True,
                    callback=self.parse)

    def parse(self, response):
        time.sleep(2)
        analisys = response.xpath('//div[@class="Pos(r) T(5px) Miw(100px) Fz(s) Fw(500) D(ib) C($primaryColor)Ta(c) Translate3d($half3dTranslate)"]/span/text()').getall()
        score = response.xpath('//div[@data-test="rec-rating-txt"]/text()').get()
        yield {'ticker': response.xpath('//h1[@class="D(ib) Fz(18px)"]/text()').get(),
               'analisys_target': analisys,
               'score': score
               }