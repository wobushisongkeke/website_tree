from __future__ import absolute_import

# DOMAIN = "jmsliu.cn"
# ORIGIN = "https://jmsliu.cn/others/m3u8%e6%b5%81%e8%a7%86%e9%a2%91%e6%95%b0%e6%8d%ae%e7%88%ac%e8%99%ab%e8%af%a6%e8%a" \
#          "7%a3%e4%b8%80%ef%bc%9am3u8%e8%a7%86%e9%a2%91%e6%96%87%e4%bb%b6%e8%af%a6%e8%a7%a3.html"
# WEBPAGE_SAVEPATH = r"E:\song\website\webpage"
# TRAVERSE_RESULT_PATH = r"E:\song\website\traverse_result.py"
# MARKDOWN_PATH = r"E:\song\website\result.md"

# the domain name of the website
DOMAIN = ["scrapy.org"]
# the start url to crawl the website
ORIGIN = "https://scrapy.org/resources/"
MAX_DEEP = None

# the folder to save the all production and mid-production
WEBPAGE_SAVEPATH = r"E:\song\website\webpage\scrapy"
TRAVERSE_RESULT_PATH = WEBPAGE_SAVEPATH + r"\traverse_result_1.py"
MARKDOWN_PATH = WEBPAGE_SAVEPATH + r"\result_1.md"