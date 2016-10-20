# WebDict
web 信息收集生成字典


程序根目录运行>> scrapy crawl tzc -a start_url=http://www.xxxxx.com -a num=100 --nolog


start_url:目标网站URL
num:爬取的网站页面上限

运行结束后，会在项目目录下生成一个以网站url命名的文件夹，里面包含了字典文件。

*如果运行报错，可能是相关模块未安装，如pyenchant,scrapy等*


@author by nmask  2015.12.1

