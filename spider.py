# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import json
import threading
import time
import random
import codecs
import csv

"""
多线程爬虫

请直接翻到最后一行，确认参数后运行

直接运行将只读取第一页，作为测试
"""



name_url="https://shandong.cncn.com/jingdian/"
useProxy = False
result = list() #最后结果
req_timeout = 10
# 集合
threadLock = threading.Lock()

"""##测试一次

获取某一页的url
"""
def getProxies():
    ips=[
        "219.151.157.130:3128",
        "222.67.189.188:9000",
        "221.219.98.141:9000",
        "219.151.142.29:3128",
        "117.114.149.66:55443",
        ]
    ip = random.choice(ips)
    return {
        'https':ip
    }

def getUserAgent():
    '''
    功能：随机获取HTTP_User_Agent
    '''
    user_agents=[
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]
    user_agent = random.choice(user_agents)
    return {
        "User-Agent":user_agent
    }


def getSiteAddress(page_number):
  global name_url
  return name_url+'1-'+str(page_number)+'-0-0.html'

"""获取bs对象"""

def getSoup(url):
  global useProxy,req_timeout
  #print(url)
  proxy = {}
  if useProxy :
    proxy = getProxies()
  response = ""
  
  try:
    response = requests.get(url,headers=getUserAgent(),proxies=proxy,timeout=req_timeout)  #生成一个response对象
    response.encoding = response.apparent_encoding #设置编码格式
    if(response.status_code==200):
      #print(response.text)#输出爬取的信息
      return BeautifulSoup(response.text,'html.parser')
        #print(str(soup))
    else:
      print("failed to get status code:"+str(response.status_code))
      return None
  except requests.exceptions.ConnectTimeout as e:        #超时
    print("Timeout: " + url + ", Proxy = "+ str(proxy))
    print(e)
    return None
  time.sleep(5)


"""从当前页面筛选合适的网址"""

def isContentAddress(addr):
  target = ".cncn.com/jingdian/"
  loca = addr.find(target)
  chosen = addr.find(target) >= 0
  #if chosen==True:
  #  print (addr+": "+str(len(addr))+", "+str(loca)+" "+str(loca+len(target) + 2))
  return chosen and len(addr) > loca+len(target)

def getInnerLinks(soup):
  inner_links=list()
  for k in soup.find_all('a',class_="pic",recursive=True):
    inner_links.append(k.get('href'))
  if(inner_links is not None):
    return list(filter(isContentAddress, list(set(inner_links))))
  #  print(len(inner_links))

"""访问过滤好的网址，并得到单个景点的dict"""

def getSingleInfo(link):
  content_soup = getSoup(link)      ##景点网址
  content_info_soup = getSoup(link+'profile') ##景点详细信息

  single_data = dict()

  single_data['name'] = content_soup.h1.text.rstrip('A')
  single_data['open_time'] = content_soup.find(text=u'开放时间：').parent.next_sibling.string
  single_data['ticket'] = content_soup.find(text=u'门票信息：').parent.next_sibling.p.get('data-title').replace('\r\n','')
  single_data['level'] = content_soup.h1.span.string
  single_data['address'] = content_soup.find('dl',class_='first').dd.text
  try:
    single_data['type'] = content_soup.find(text=u'景点类型：').parent.next_sibling.a.string
  except:
    single_data['type'] = ""

  #descr = content_soup.find('dl',class_='introduce').dd.text[0:14]
  single_data['descr'] = content_info_soup.find_all(text=re.compile("简介："))[0].parent.parent.next_sibling.next_sibling.text
  
  return single_data

"""扫描单个页面"""

def getInfoAndAddToRestltList(inner_links, page_number = 0, thread_no = 0):
  global result,threadLock
  count = 1
  for link in inner_links:
    content_dict = getSingleInfo(link)
    threadLock.acquire()
    result.append(content_dict)
    print("[线程 "+str(thread_no)+"] 已爬取第 "+str(page_number)+" 页的 \""+content_dict['name']+'"('+str(count)+'/'+str(len(inner_links))+')')
    threadLock.release()
    count = count + 1

def startPageScan(page_number, thread_no = 0):
  #try:
  
  soup = getSoup(getSiteAddress(page_number))   #获取某页的soup

  #except:
  #  print("proxy error")
  #  return None
  #print(str(soup))
  inner_links = getInnerLinks(soup)             #该页面下的所有link
  #print(len(inner_links))
  getInfoAndAddToRestltList(inner_links, page_number, thread_no)        #每一个link的
  #print(len(result))

"""线程分发"""

def scanWorker(thread_no, total_thread , total_page):    ##thread_no starts from 0

  current_page = thread_no + 1
  while current_page <= total_page :
    #print("线程 "+str(thread_no)+" ，当前在 "+str(current_page)+" 页")
    res = startPageScan(current_page, thread_no)
    print("[线程 "+str(thread_no)+"] 第 "+str(current_page)+" 页已全部完成")
    current_page = current_page + total_thread
  
def exportCSV(filename):
	global result
	"""
	result = list()
	result.append({'为':'王薇薇','哈哈哈':'33额'})
	result.append({'为':'事实上','哈哈哈':'11岁'})
	"""
	if len(result) == 0:
		print('结果为空！')
		return None
	with open(filename, 'w', encoding='utf-8',newline='',errors='ignore') as file_obj:
		writer = csv.writer(file_obj)
		writer.writerow(result[0].keys())
		for single_info in result:
			writer.writerow(single_info.values())
	print('[Spider] 已将结果CSV写入文件 '+filename)

def exportJson(filename):
	global result
	
	with codecs.open(filename,'w',encoding='utf-8',errors='ignore') as file_obj:
		#json.dump(result,file_obj,ensure_ascii=False)
		file_obj.write(json.dumps(result,ensure_ascii=False,indent=4))
	print("[Spider] 已将结果JSON写入文件 " + filename)
	
"""主程序"""

def startScan(start_page, total_page, total_thread, use_proxy, timeout, export_file_name):
    
    global useProxy,req_timeout
    useProxy = use_proxy
    req_timeout = timeout

    jobs = []

    for i in range(total_thread):
      th = threading.Thread(target=scanWorker, args=(i,total_thread,total_page))
      jobs.append(th)
      th.start()
    for thread in jobs:
    	thread.join()
    	
    if export_file_name.endswith('.csv'):
    	exportCSV(export_file_name)
    else:
    	exportJson(export_file_name)	#export file
    

### 从这里开始，在这里设置参数
startScan(
	start_page = 1, 											#从第1页开始爬数据
	total_page = 4, 											#总页数，看网站上应该是86，网络不稳定的话也可以分多次下载
	total_thread = 1,											#线程数，谨慎修改，爬得太快容易封IP
	use_proxy = False,										#如果被封IP，就需要设置代理，将这里设置为True，同时在getProxies函数中添加可用的IP地址
	timeout = 20,													#每个页面的加载时限
	export_file_name = 'cncn_result.csv'	#最后生成的文件
)

#exportCSV('1.csv')
"""多线程

输出json
"""
