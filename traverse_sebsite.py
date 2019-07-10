"""Due to the long duration of crawling, we keep the traversing program isolated."""
from url_object import UrlObject
from selenium import webdriver
from selenium.webdriver import ChromeOptions as Options

import settings


def traverse_website():

    """ An example to use the origin webpage to traverse the website"""

    ORIGIN = settings.ORIGIN
    TRAVERSE_RESULT_PATH = settings.TRAVERSE_RESULT_PATH
    MAX_DEEP = settings.MAX_DEEP

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    prefs = {'profile.managed_default_content_settings.images': 2}
    chrome_options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(chrome_options=chrome_options)

    index = []
    document = {}
    origin = UrlObject(ORIGIN, browser)

    index.append(origin)
    document[origin.url] = origin

    for obj in index:
        if MAX_DEEP is not None and obj.deep > MAX_DEEP:
            continue
        obj.crawling()
        document[obj.url] = obj
        if obj.deep == MAX_DEEP:
            pass
        else:
            for i in range(obj.inner_link_count):
                if obj.inner_link[i] not in document:
                    in_item = UrlObject(obj.inner_link[i], browser, obj.url, obj.deep+1)
                    index.append(in_item)
                    document[obj.inner_link[i]] = in_item
                else:
                    uo = document[obj.inner_link[i]]
                    uo.refering(obj.url)

    with open(TRAVERSE_RESULT_PATH, "w") as f:
        f.write("from __future__ import absolute_import\n\n")
        f.write("index = [")
        for obj in index:
            #print(obj.__dict__)
            obj.__dict__.pop('browser', 404)
            f.write(str(obj.__dict__))
            f.write(",")
        f.write("]")

    browser.close()

if __name__ == "__main__":
    traverse_website()
