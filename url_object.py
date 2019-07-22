import traceback
import os
import logging

from urllib.parse import urljoin
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver import ChromeOptions as Options

import settings

DOMAIN = settings.DOMAIN
WEBPAGE_SAVEPATH = settings.WEBPAGE_SAVEPATH

logging.basicConfig(filename="test.log", filemode="w+", format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S", level=logging.INFO)


class UrlObject:

    """a data structure to save the information of every webpage"""

    def __init__(self, url, browser, referer=None, deep=1, filepath=WEBPAGE_SAVEPATH):
        self.browser = browser

        self.url = url.lower()
        up = urlparse(self.url)
        if up.scheme == "http":
            self.url = self.url[7:]
        elif up.scheme == "https":
            self.url = self.url[8:]
        if self.url.endswith("/"):
            self.url = self.url[:-1]
        self.origin_url = self.url

        self.referer = []
        if referer is not None:
            up = urlparse(referer)
            if up.scheme == "http":
                referer = referer[7:]
            elif up.scheme == "https":
                referer = referer[8:]
            self.referer.append(referer.lower())
        self.referer_count = len(self.referer)

        self.deep = deep

        self.crawled = False

        self.inner_link = []
        self.inner_link_count = len(self.inner_link)

        self.outer_link = []
        self.outer_link_count = len(self.outer_link)

        self.filepath = filepath
        if not os.path.exists(self.filepath):
            os.makedirs(self.filepath)

    def _real_url(self, url):
        if url.startswith("http"):
            return url
        return urljoin(self.url, url)

    def crawling(self):
        print("crawling ", self.url)
        try:

            self.browser.get("https://" + self.origin_url)
            curr_url = self.browser.current_url
            up = urlparse(curr_url)
            if up.netloc not in DOMAIN:
                DOMAIN.append(up.netloc)
            self.url = curr_url

            url_list = self.browser.find_elements_by_xpath("//a")
            for url in url_list:
                str_url = str(url.get_attribute("href"))
                str_url = str_url.split("#")[0]
                str_url = self._real_url(str_url).lower()
                u_domain = urlparse(str_url).netloc
                up = urlparse(str_url)
                if up.scheme == "http":
                    str_url = str_url[7:]
                elif up.scheme == "https":
                    str_url = str_url[8:]
                if str_url.endswith("/"):
                    str_url = str_url[:-1]
                if u_domain in DOMAIN:
                    self.inner_link.append(str_url)
                    self.inner_link_count += 1
                else:
                    self.outer_link.append(str_url)
                    self.outer_link_count += 1

            filename = self.url.split("/")[-1]
            if len(filename) == 0:
                filename = self.url.split("/")[-2]
            filename = filename.split(".")[0] + ".html"
            filename = filename.replace("?", "_").replace("\\", "_").replace("*", "_").replace("\"", "_")\
                .replace("<", "_").replace(">", "_").replace("|", "_").replace("/", "_").replace(":", "_")
            while os.path.exists(os.path.join(self.filepath, filename)):
                filename = filename.split(".html")[0] + "(1).html"
            with open(os.path.join(self.filepath, filename), "wb") as f:
                f.write(self.browser.page_source.encode("utf-8", "ignore"))
            self.crawled = True

            logging.info("crawling " + self.url)

        except:
            logging.warning("exception " + self.url)
            traceback.print_exc()

    def refering(self, url):
        up = urlparse(url)
        if up.scheme == "http":
            url = url[7:]
        elif up.scheme == "https":
            url = url[8:]
        self.referer.append(url.lower())
        self.referer_count = len(self.referer)


def create_uo():

    """An example to get the information of a webpage"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)

    uo = UrlObject("https://jmsliu.cn/others/m3u8%e6%b5%81%e8%a7%86%e9%a2%91%e6%95%b0%e6%8d%ae%e7%88%ac%e8%99%ab%e8%af%"
                   "a6%e8%a7%a3%e4%b8%89%ef%bc%9am3u8%e8%a7%86%e9%a2%91%e7%bd%91%e7%bb%9c%e6%95%b0%e6%8d%ae%e7%88%ac%e8"
                   "%99%ab%e5%ae%9e%e7%8e%b0.html", browser)
    uo.crawling()
    print(uo.__dict__)
    browser.close()


if __name__ == "__main__":
    create_uo()
