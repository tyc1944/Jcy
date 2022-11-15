import time

import scrapy
from bs4 import BeautifulSoup
from Jcy.items import JcyItem
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, ui


class JcySpider(scrapy.Spider):
    name = 'Jcy'
    allowed_domains = ['wenshu.court.gov.cn/']
    start_url = ['https://wenshu.court.gov.cn/website/wenshu/181010CARHS5BS3C/index.html?open=login']
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    # options.add_argument('user-agent=%s' % self.user_agents)
    driver = webdriver.Chrome(options=options)
    def start_requests(self):
        self.driver.get(self.start_url[0])
        time.sleep(2)
        username = self.driver.find_element_by_xpath('//*[@id="root"]/div/form/div/div[1]/div/div/div/input')
        username.send_keys("17605102938")
        password = self.driver.find_element_by_xpath('//*[@id="root"]/div/form/div/div[2]/div/div/div/input')
        password.send_keys("Tyc194413")
        self.driver.find_element_by_xpath('//*[@id="root"]/div/form/div/div[3]/span').click()
        self.driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/span[2]').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="_view_1540966819000"]/div/ul/li[3]/a').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="j4_1_anchor"]')
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="A00"]/i').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="A20_anchor"]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="j20_1_anchor"]').click()
        time.sleep(1)
        yield scrapy.Request(self.driver.current_url, callback=self.fanye)

    def fanye(self, response):
        listNumber = self.driver.find_element_by_xpath('//*[@id="_view_1545184311000"]/div[1]/div[2]/span').string
        onePageCount = 5
        total = listNumber / onePageCount + 1
        for i in range(1, int(total + 1)):
            if i>1:
                print('获取下一页数据')
                self.driver.find_element_by_xpath('//*[@id="_view_1545184311000"]/div[8]/a[last()]').click()
                yield scrapy.Request(self.driver.current_url, callback=self.parse)
            else:
                yield scrapy.Request(self.driver.current_url, callback=self.parse)

    def parse(self, response):
        """
        抓取列表页
        :param response:
        :return:
        """
        soup = BeautifulSoup(response.text, 'lxml')
        list = soup.findAll(class_='LM_list')

        for link in list:
            url = link.select('#_view_1545184311000 > div:nth-child(3) > div.list_title.clearfix > h4 > a')
            yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        """
        解析selenium加载完成之后的详情页
        :param response:
        :return:
        """
        item = JcyItem()

        url = response.url
        date = response.xpath('//*[@id="_view_1541573883000"]/div/div[1]/div[1]').string
        title = response.xpath('//*[@id="_view_1541573883000"]/div/div[1]/div[1]').string
        content = response.xpath('//*[@id="_view_1541573883000"]/div/div[1]/div[3]').string

        yield item

    # def close(self, spider):
    #     self.driver.quit()
