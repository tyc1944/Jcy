# coding=utf-8

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, ui
from bs4 import BeautifulSoup
import xlwt
# from settings import *
import time
import requests
from selenium.common.exceptions import StaleElementReferenceException
# browser = webdriver.PhantomJS()

book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('jiandawang', cell_overwrite_ok=True)
sheet.write(0, 0, '名称')
sheet.write(0, 1, '内容')
n = 1


def getDriver():
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    # user_ag = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
    # options.add_argument('user-agent=%s' % user_ag)
    options.add_argument("--disable-blink-features=AutomationControlled")

    global browser
    browser = webdriver.Chrome(options=options)
    global WAIT
    WAIT = WebDriverWait(browser, 10)
    browser.set_window_size(1400, 900)
    # browser.execute_cdp_cmd("Network.enable", {})
    # browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    return browser


def search():
    try:
        print('开始访问正义智库....')

        browser.get("http://jianda.gj.jcy/admin/login/auth")
        username = browser.find_element_by_name("username")
        username.send_keys("320203198603022534")
        password = browser.find_element_by_name("password")
        password.send_keys("1986.3.2Qc")
        know = browser.find_element_by_xpath('//*[@id="check1"]')
        know.click()
        login = browser.find_element_by_xpath('//*[@id="loginForm"]/div[4]/button')
        login.click()
        time.sleep(1)
        image = browser.find_element_by_xpath('/html/body/main/div[2]/div[2]/img[2]')
        wait = ui.WebDriverWait(browser, 10)
        image.click()
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[-1])
        sreach_window3 = browser.current_window_handle
        browser.execute_script("window.scrollBy(0,5000)")
        browser.find_element(By.CSS_SELECTOR, "div.w1440.resources > ul > li:nth-child(3) > a > img").click()
        browser.switch_to.window(browser.window_handles[-1])
        anli = browser.find_element_by_xpath('//*[@id="fyy_lajs"]')
        anli.click()
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[-1])
        time.sleep(1)
        browser.find_element_by_css_selector('#casecause-wrapper > div > div.secLevel > ul > li:nth-child(6)').click()
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="casecause-wrapper"]/div/div[2]/div/div/ul/li[1]/a/span/i').click()
        browser.switch_to.window(browser.window_handles[-1])
        browser.execute_script("window.scrollBy(0,8000)")
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="nav-province"]/div/dl/dd[11]/span/i').click()
        time.sleep(3)
        browser.find_element_by_xpath('//*[@id="nav-province"]/div/dl/dd[11]/dl/dd[3]/span').click()
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="nav-judgeyear"]/div/dl/dd[2]').click()
        time.sleep(1)
        get_source()
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[-1])
        total = browser.find_element(By.XPATH, '//*[@id="result-top"]/dl/dd[5]/b')
        if int(total.text)%10==0:
            total1=int(total.text)/10
            return total1
        else:
            total1= int(int(total.text)/10)+1
            return total1

    except TimeoutException:
        return search()


def next_page(page_num):
    try:
        print('获取下一页数据')
        browser.switch_to.window(browser.window_handles[-1])
        time.sleep(3)
        next_btn = WAIT.until(EC.element_to_be_clickable((By.XPATH,
                                                          '//*[@id="pagination"]/a[last()]')))
        next_btn.click()
        WAIT.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                                                     '#pagination > span'),
                                                    str(page_num)))
        time.sleep(1)
        get_source()
    except TimeoutException:
        browser.refresh()
        return next_page(page_num)


def save_to_excel(soup, n):
    WAIT.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="title"]/h2')))
    #WAIT.until(lambda browser: browser.find_element_by_xpath('//*[@id="title"]/h2'))
    print(soup.find(id='title').h2.text+"+++++++++++++==")
    item_title = soup.find(id='title').h2.text
    item_date = soup.find(id='info').text
    sheet.write(n, 0, item_title)
    sheet.write(n, 1, item_date)
    browser.close()


def get_source():
    print('到这')
    browser.switch_to.window(browser.window_handles[-1])
    # result-items > div:nth-child(1) > div.r-title > h4 > p > span
    # result-items > div:nth-child(3) > div.r-title > h4 > p > span
    elements = browser.find_elements(By.CSS_SELECTOR, '.r-title > h4 > p > span')
    length=len(elements)
    for i in range(0, length):  # 遍历列表的循环，使程序可以逐一点击.r-title
        browser.switch_to.window(browser.window_handles[-1])
        elements = browser.find_elements(By.CLASS_NAME, 'r-title')
        print(len(elements))
        # try:
        WAIT.until(EC.presence_of_element_located((By.CLASS_NAME, 'result_item')))
        browser.execute_script("arguments[0].scrollIntoView();", elements[i])
        link = elements[i]
        print(link.string)
        if link.string == "2678程建平劳动争议二审民事裁定书":
            js = "window.open('http://143.3.143.144:8088/shaanxi/page/result.html?type=b&backurl=http://143.3.143.140/')"
            browser.execute_script(js)
        else:
            link.click()
        # except StaleElementReferenceException as msg:
        #     print(msg)
        #     WAIT.until(EC.presence_of_element_located((By.CLASS_NAME, 'result_item')))
        #     browser.execute_script("arguments[0].scrollIntoView();", elements[i])
        #     link = elements[i]
        #     link.click()
        time.sleep(2)  # 留出加载时间
        browser.switch_to.window(browser.window_handles[-1])
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        global n
        save_to_excel(soup, n)
        n = n + 1


def main():
    driver = getDriver()
    total = search()
    print(total)

    for i in range(2, int(total + 1)):
        next_page(i)


if __name__ == '__main__':
    main()
    book.save('正义智库.xlsx')
