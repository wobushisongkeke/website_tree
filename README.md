# website_tree
本项目为网站树形结构生成，包括从源网页遍历整个网站，对网站中各个网页节点信息分析生成树形结构，以及生成树形结构对应的.md文件。为演示效果，可将.md导入百度脑图中可视化效果。为教学讲解用使用Scrapy官网作为示例，仅做技术讲解用，不涉及和教唆任何非法获取数据，非法使用数据，和非法占有数据的行为。对于没有经过授权的数据爬取行为都是违规的！对于任何个人，团体或者机构，使用该技术从事任何违法违规行为的，自担风险。

## 使用方法
将本项目下载到本地。

修改`settings.py`

运行`traverse_sebsite.py`

将`traverse_result_1.py`从目标路径copy至当前路径中。

运行`build_tree.py`

将`.md`文件导入[百度脑图](http://naotu.baidu.com/)查看效果

##代码介绍

### settings.py
存放配置内容，其中：

`DOMAIN`为整个网站的域名，用来判别网页中的url是否属于本网站，若属于则爬取，否则，跳过。是一个list型变量，为了解决重定向问题。

`ORIGIN`为爬取的起点，也就是从该网页开始进行爬取。

`MAX_DEEP`为爬取深度，也就是从`ORIGIN`开始爬取几层，若为None，则爬取整个网站。

`WEBPAGE_SAVEPATH`为爬取时保存的静态网页路径。

`TRAVERSE_RESULT_PATH`为爬取后保存的节点信息路径。

`MARKDOWN_PATH`为生成网站树后保存的.md文件路径。

###url_object.py
保存每个url节点的信息

其中`self.url`和`self.origin_url`分别对应当前网页的重定向后的url和原始url。`self.referer`和`self.referer_count`分别对应访问此url的url列表及总个数。`self.deep`表示从爬取起点到此url的层数。`self.crawled`表示此节点是否被爬取过。`self.inner_link`和`self.inner_link_count`表示此url中内部链接的列表及个数。`self.outer_link`和`self.outer_link_count`表示此url中外部链接的列表及个数。`self.filepath`表示当前url的下载路径。

对于没被爬取过的网页，调用`crawling()`函数来进行爬取，对于已经爬取的网页调用`refering()`函数来改变referer。

### traverse_sebsite.py
遍历网站

###traverse_result_1.py
为遍历网站后的节点信息，需要从目标路径copy至当前路径中。

### build_tree.py
遍历节点信息，生成树形结构及.md文件。

### .md
为生成的树形结构的表示方式，可导入百度脑图，形成可视化。

### .svg
从百度脑图中导出的可视化效果，也可导成其他格式。

## 关于我们
作者为研二程序媛一枚，在爬虫方面也还是一个新手，如有不足之处请见谅。如果大家对本项目有任何建议，想法或者问题，欢迎交流和探讨。