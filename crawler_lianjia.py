# -*- encoding=utf8 -*-
##从链家网站获取感兴趣小区的价格

##网页地址类型：http://sh.lianjia.com/ershoufang/rs<小区名称>
# python version:2.7
# bs4 version: 4.4.0

from bs4 import BeautifulSoup
import codecs
import urllib2
import re
from operator import itemgetter 
import datetime,time
import os



def get_str(u_item):
    if isinstance(u_item,unicode):
        return u_item.encode('utf-8')
    elif isinstance(u_item,str):
        return u_item
    else:
        return str(u_item)

def get_unicode(u_item):
    if isinstance(u_item,unicode):
        return u_item
    elif isinstance(u_item,str):
        return u_item.decode('utf-8')
    else:
        return str(u_item.decode('utf-8'))

def savePriceInfo(curpriceDict,name,filename):
    
    writeFile=codecs.open(filename,'a','utf-8')

    name_unicode = get_unicode(name)
    writeFile.write(name_unicode +'\n')
    for tag  in curpriceDict:
        writeFile.write(tag['area']+u'平米'+'\t'+tag['price']+u'万'+'\n')
    writeFile.close()

#parse the price and area info 
def parseHtmlUserId(html):
    priceDict=[]
    soup=BeautifulSoup(html,"html.parser")

    ##<span class="meters">57平米</span>
    ##<div class="price"><span class="num">230</span>万</div>
    meters_tags=soup.findAll('span',class_='meters')
    price_tags=soup.findAll('div',class_='price')

    for meter,price in zip(meters_tags,price_tags):
        price = re.findall(r'<span class="num">(\d+)</span>',str(price.find_all('span')))
        area = re.findall(r"(\d+)\\u5e73\\u7c73",str(meter.contents))

        priceDict.append({'area':area[0],'price':price[0]})
    
    return sorted(priceDict,key=itemgetter('price'))


def getHtml(url):
    page=urllib2.urlopen(url)
    html=page.read()
    return html

def launch(urlList):
    now = time.strftime("%Y_%m_%d_%H_%M")
    filename = 'priceList_'+now+'.txt'
    for url in urlList:
        name = re.findall(ur'/rs(.*?)$',url)[0]
        html=getHtml(url)
        print 'parse ' + get_str(name) + '...'
        (curpriceDict)=parseHtmlUserId(html)
        savePriceInfo(curpriceDict,name,filename)
        time.sleep(2)

def main():
    baseUrl='http://sh.lianjia.com/ershoufang/rs'

    if (not os.path.isfile("nameList.txt")):
        print "ERROR: can't find the input file nameList.txt which have the name of community"
        return

    with open('nameList.txt','rt') as f:
        nameList = f.read().split('\n')

    for name in nameList:
        print get_str(name)

    urlList = [baseUrl+name.strip() for name in nameList]

    print urlList
    launch(urlList)

if __name__ == '__main__':
    main()

