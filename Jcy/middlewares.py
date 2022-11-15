# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class JcySpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JcyDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

import scrapy
from scrapy import signals

from selenium import webdriver
from settings import *
from scrapy.utils.project import get_project_settings

# settings = get_project_settings()
# 驱动selenium中间件
# class SeleniumMiddleware(object):
#     def __init__(self):
#        # self.driver = webdriver.Chrome()
#         self.user_agents = DEFAULT_REQUEST_HEADERS['USER_AGENTS']
#
#     def process_request(self, request, spider):
#         options = webdriver.ChromeOptions()
#         options.add_argument("--disable-extensions")
#         options.add_argument("--disable-gpu")
#         options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         options.add_experimental_option("useAutomationExtension", False)
#         options.add_argument('user-agent=%s' % self.user_agents)
#         driver = webdriver.Chrome(options=options)
#         if request.url == r'https://wenshu.court.gov.cn/website/wenshu/181010CARHS5BS3C/index.html?open=login':
#             driver.get(request.url)
#             time.sleep(2)
#             username = driver.find_element_by_xpath('//*[@id="root"]/div/form/div/div[1]/div/div/div/input')
#             username.send_keys("17605102938")
#             password = driver.find_element_by_xpath('//*[@id="root"]/div/form/div/div[2]/div/div/div/input')
#             password.send_keys("Tyc194413")
#             driver.find_element_by_xpath('//*[@id="root"]/div/form/div/div[3]/span').click()
#             driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/span[2]').click()
#             time.sleep(2)
#             driver.find_element_by_xpath('//*[@id="_view_1540966819000"]/div/ul/li[3]/a').click()
#             time.sleep(2)
#             driver.find_element_by_xpath('//*[@id="j4_1_anchor"]')
#             time.sleep(2)
#             driver.find_element_by_xpath('//*[@id="A00"]/i').click()
#             time.sleep(1)
#             driver.find_element_by_xpath('//*[@id="A20_anchor"]').click()
#             time.sleep(1)
#             driver.find_element_by_xpath('//*[@id="j20_1_anchor"]').click()
#             time.sleep(1)
#         html = self.driver.page_source
#         return scrapy.http.HtmlResponse(url=self.driver.current_url, body=html.encode("utf-8"),
#                                         encoding="utf-8", request=request)


