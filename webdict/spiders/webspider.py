#!coding = utf-8
from bs4 import BeautifulSoup
import re
from scrapy import Spider
import scrapy
from scrapy.spiders import Rule   
#from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
import enchant
import urlparse
import os
import shutil

'''
[HELP]  scrapy crawl tzc -a start_url=http://www.hzxh.gov.cn -a num=100 --nolog
'''

class testSpider(Spider):
	name = "tzc"
	rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths = ('.//a')), callback="parse_items" , follow = True)
        	)


	def __init__(self,*args,**kwargs):
		super(testSpider,self).__init__(*args,**kwargs)   
		self.can = [kwargs.get("start_url"),kwargs.get("num")]  
		self.url=self.can[0]
		self.num=self.can[1]
		self.domain=urlparse.urlparse(self.url).netloc
		self.allowed_domains=[self.domain]                  #allowed_domains
		self.start_urls=[self.url]                          #start_url
		self.list_abbr=[]
		self.list_name=[]
		self.list_year=[]
		self.list_email=[]
		self.x=0

	def close(self,reason):
		try:           
			d=enchant.Dict("en_US")
			key=['www','http','https','icp','ppp','htm','html','edu','cctv','internet','dna','facebook','ceo','asp','aspx','php','jsp',
			'jspx','gdp','javascript','chinese','xml','jquery','pdf','rss','href','app','xls','ppt','gps','english','ipad','microsoft',
			'png','src']
			self.list_abbr=list(set([x.lower() for x in self.list_abbr]))
			self.list_name=list(set([x.lower() for x in self.list_name]))
			self.list_name=[x for x in self.list_name if d.check(x) == False ]
			self.list_abbr=[x for x in self.list_abbr if d.check(x) == False ]
			for i in key:
				try:
					self.list_abbr.remove(i)
				except:
					pass
			print 'abbr:',self.list_abbr
			print 'name:',self.list_name
			print 'year:',self.list_year
			print 'email:',self.list_email


			if os.path.exists("./"+self.domain):       #delete file
				shutil.rmtree("./"+self.domain)

			os.mkdir('./'+self.domain)

			f_abbr=open(self.domain+'/abbr.txt','a')
			f_name=open(self.domain+'/name.txt','a')
			f_email=open(self.domain+'/email.txt','a')
			f_year=open(self.domain+'/year.txt','a')

			for i in self.list_abbr:
				f_abbr.write(i+'\n')
			for i in self.list_name:
				f_name.write(i+'\n')
			for i in self.list_email:
				f_email.write(i+'\n')
			for i in self.list_year:
				f_year.write(i+'\n')

			f_abbr.close()
			f_name.close()
			f_email.close()
			f_year.close()
		except Exception,e:
			print e

	def parse(self, response):   
		if self.x<int(self.num):
			try:
				self.x+=1
				for href in response.xpath(".//a/@href").extract():
					request = scrapy.Request(self.url+href,callback=self.parse)
					print "[*]%s" % (self.url+href)
					yield request	
			except:
				pass
			try:
				soup=BeautifulSoup(response.body)                              
				[script.extract() for script in soup.findAll('script')]
				[style.extract() for style in soup.findAll('style')]
				reg1 = re.compile("<[^>]*>")
				content = reg1.sub('',soup.prettify()).replace('\n','')
				res_year=r'[1][9][9][0-9]{2}|[2][0][0-9]{2}'                     
				res_abbr=r'[a-zA-Z]{3,14}'
				res_name=r'((?:[A-Za-z][a,e,h,u,i,o]{1,4}){2,3})[^a-zA-Z]'
				res_email=r'(\w{1,20}@\w{1,10}\.\w{1,10}\.?\w*)'

				p_year=re.compile(res_year)
				self.list_year=list(set(self.list_year+list(set(p_year.findall(content)))))

				p_abbr=re.compile(res_abbr)
				self.list_abbr=list(set(self.list_abbr+list(set(p_abbr.findall(content)))))

				p_name=re.compile(res_name)
				self.list_name=list(set(self.list_name+list(set(p_name.findall(content)))))

				p_email=re.compile(res_email)
				self.list_email=list(set(self.list_email+list(set(p_email.findall(content)))))

				#sys.stdout.write('[*]page number:%s \r' % str(self.x))
				#sys.stdout.flush()
			except Exception,e:
				print e
				pass
		else:
			pass
