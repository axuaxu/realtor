# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.parser import parse
from dateutil.relativedelta import *
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import requests
import codecs
from lxml import html
import sqlite3
import re
from random import randint

def xchar(instr):
    tstr = " ".join(re.findall("[a-zA-Z]+", instr))
    outstr = ''.join(tstr)
    return outstr

def xnum(innum):
    tnum = " ".join(re.findall("\d+", innum))
    outnum = ''.join(tnum)
    return outnum


def setFields(udate,surl,area,sparser,c,conn):
    num = surl.rsplit('/',1)[1]
    num = num.split('.',1)[0]
    title = sparser.xpath('//span[@class="detail_top_title_text"]/text()')[0]
    #atitle = " ".join(re.findall("[a-zA-Z]+", title[0]))
    atitle = xchar(title)
    tprice = sparser.xpath('//span[@class="detail_top_title_price"]/text()')
    wprice = " ".join(tprice[0].split())
    lprice = wprice.replace(',','')
    aprice = xnum(lprice)
    #rprice = re.findall('\d+',lprice)
    #try:
    #   aprice = rprice[0]    
    #except IndexError:
    #        aprice = 0

    address = sparser.xpath('//div[@class="detailinfosubtitle"]/text()')
    waddress = " ".join(address[0].split())
    pcode = waddress[-7:]
    
    wrent = '' 
    wlength = ''
    wtenant = ''
    wrooms = ''
    abus = ''
    ametro = ''
    atrain = ''
    ahway = ''
    wtreq = ''
    wcondition = ''
    wequip = ''
    wenv = ''
    wbus = ''
    wmetro = ''
    wtrain = ''
    whway = ''
    wname = ''
    sphone = ''
    sphone2 = ''
    semail = ''
    swechat = ''
    sqq = ''
        
    for item in sparser.xpath('//div[@id="detailpage_left_side"]/div[1]/ul/li'):
        tt = item.xpath('./span/text()')
        if not tt:
           print 'empty list'
           continue
        pp = item.xpath('./text()')
        #print pp[1] 
        try:
            detail = " ".join((tt[0]+pp[1]).split())
            #print detail
        except IndexError:
            continue
        if u'每月租金' in tt[0]:
           wrent =  " ".join(pp[1].split())
        if u'房屋类型' in tt[0]:
           wstyle =  " ".join(pp[1].split())
        if u'出租方式' in tt[0]:
           wmethod =  " ".join(pp[1].split())
        if u'周边信息' in tt[0]:
           wcircle =  " ".join(pp[1].split())
        if u'出租房间' in tt[0]:
           wrooms =  " ".join(pp[1].split())
        if u'租约长短' in tt[0]:
           wlength =  " ".join(pp[1].split())
        if u'入住时间' in tt[0]:
           wintime =  " ".join(pp[1].split())
        if u'出租对象' in tt[0]:
           wtenant =  " ".join(pp[1].split())
        if u'使用条件' in tt[0]:
           wcondition =  " ".join(pp[1].split())
        if u'房客要求' in tt[0]:
           wtreq =  " ".join(pp[1].split())
        if u'附属设施' in tt[0]:
           wequip =  " ".join(pp[1].split())
        if u'周边环境' in tt[0]:
           wenv =  " ".join(pp[1].split())
        if u'附近公车' in tt[0]:
           wbus =  " ".join(pp[1].split())
           abus = xnum(wbus)
        if u'附近地铁' in tt[0]:
           wmetro =  " ".join(pp[1].split())
           ametro = xchar(wmetro)
        if u'附近火车' in tt[0]:
           wtrain =  " ".join(pp[1].split())
           atrain = xchar(wtrain) 
        if u'附近高速' in tt[0]:
           whway =  " ".join(pp[1].split())
           ahway = xnum(whway)
        ldesc = sparser.xpath('//div[@id="summary"]/text()')
        k  = 0
        desc = ''
        while k<len(ldesc):
            desc = desc + ldesc[k]
            k = k+1

        oname = sparser.xpath('//div[@class="detail_agent_companyname"]/span/text()')
        try:
            wname = oname[0]
        except IndexError:
            wname = ''
        phone = sparser.xpath('//div[@class="detail_agent_phone"]/span[1]/text()')
        email = sparser.xpath('//div[@class="detail_agent_emali"]/a/text()')
        wechat = sparser.xpath('//div[@class="detail_agent_wechat"]/a/text()')
        qq = sparser.xpath('//div[@class="detail_agent_qq"]/a/text()')
        sphone = ''.join(phone)
        sphone2 = ''
        semail = ''.join(email)
        swechat = ''.join(wechat)
        sqq = ''.join(qq)
        #sphone = str(phone)
        #semail = str(email)
        #sphone = sphone.replace('[','')
        #sphone = sphone.replace(']','')
        #sphone = sphone.replace("'","",2)

        #semail = semail.replace('[','')
        #semail = semail.replace(']','')
        #semail = semail.replace("'","",2)


    print aprice,pcode,num,title,wprice,atitle,ametro,abus,waddress,wrent,wrooms,wintime,wname,sphone,wechat
    
    sinsert1 = 'insert into monrent( "num", "udate", "surl","title", "address", "pcode","rent", "rstyle", "method", "rooms", "length", "intime", "desc", "tenant", "treq", "condition", "equip", "env", "bus", "metro","train", "hway", "oname", "phone",  "phone2", "email","wechat","qq" ,"aprice","atitle","abus","ametro","atrain","ahway","area1","area2","area3" )'
    sinsert2 = 'values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    sinsert = sinsert1+sinsert2
    svalues = 'num, udate, surl,title, waddress,pcode, wrent, wstyle, wmethod, wrooms, wlength,wintime, desc, wtenant, wtreq, wcondition, wequip, wenv, wbus, wmetro,wtrain, whway, wname, sphone,  sphone2, semail,swechat,sqq ,aprice,atitle,abus,ametro,atrain,ahway,'
    c.execute(sinsert,(num, udate, surl,title, waddress,pcode, wrent, wstyle, wmethod, wrooms, wlength,wintime, desc, wtenant, wtreq, wcondition, wequip, wenv, wbus, wmetro,wtrain, whway, wname, sphone,  sphone2, semail,swechat,sqq ,aprice,atitle,abus,ametro,atrain,ahway,area[0],area[1],area[2]))
    conn.commit()

    #pass

sqlite_file = "montreal.sqlite"
conn = sqlite3.connect(sqlite_file)
conn.text_factory = bytes
c = conn.cursor()

murl = 'http://www.iu91.com/rs/rent'

driver = webdriver.Firefox()
driver.get(murl)
#assert "Python" in driver.title
elem = driver.find_element_by_class_name("showSwitcher")
#elem.clear()
elem.send_keys("QC")
elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source

parser = html.fromstring(driver.page_source,driver.current_url)

today = datetime.now()
udate = ''
base = 'http://www.iu91.com'
area = ['','','']

for i in range(1,20):
    
    for j in range(1,31):
        xtype = '//*[@id="listArea"]/ul/li['+str(j)+']/div/div[2]/div[3]/text()'
        rtype = parser.xpath(xtype)
        if (u'客栈' in rtype[0]) or (u'车位' in rtype[0]) or (u'办公室' in rtype[0]) or (u'店面' in rtype[0]) or (u'厂房' in rtype[0]) or (u'仓库' in rtype[0]) or (u'土地' in rtype[0]):
            print 'short term hotel',rtype[0]
            continue
        #if u'车位' in rtype[0]:
        #    print 'parking lot',rtype[0]
        #    continue
        #if u'办公室' in rtype[0]:
        #    print 'parking lot',rtype[0]
        #    continue

        xlink = '//*[@id="listArea"]/ul/li['+str(j)+']/div/div[2]/div[1]/span/a/@href'
        rlink = parser.xpath(xlink)
        print j,rlink[0]
        xtime = '//*[@id="listArea"]/ul/li['+str(j)+']/div/div[2]/div[5]/text()'
        utime = parser.xpath(xtime)
        print utime[0]
        if u'当天更新' in utime[0]:
           udate = str(today)[:10]
        else:
            if u'昨天更新' in utime[0]:
               udate = str(today+relativedelta(days=-1))[:10]
            else:
               if u'前天更新' in utime[0]:
                  udate = str(today+relativedelta(days=-2))[:10]
               else:
                   try:
                      found = re.findall('\d+',utime[0])
                      ff = int(found[0])
                   except AttributeError:
                      ff = 0
                   #m = re.search("\d+",utime[0])
                   #if m:
                   udate = str(today+relativedelta(days=-ff))[:10]
        print udate

        #.//*[@id='listArea']/ul/li[10]/div/div[2]/div[4]/a[1]
        #for area in parser.xpath('//*[@id="listArea"]/ul/li[10]/div/div[2]/div[4]/a[1]')
        #for aitem in parser.xpath('//*[@id="listArea"]/ul/li[10]/div/div[2]/div[4]'):
        #    area[ai-1]=(aitem.xpath('./a['+str(ai)+']/text()'))[0]
        #    ai = ai+1
        
        area[0] = parser.xpath('//*[@id="listArea"]/ul/li[15]/div/div[2]/div[4]/a[1]/text()')[0]
        area[1] = parser.xpath('//*[@id="listArea"]/ul/li[15]/div/div[2]/div[4]/a[2]/text()')[0]
        try :
            area[2] = parser.xpath('//*[@id="listArea"]/ul/li[15]/div/div[2]/div[4]/a[3]/text()')[0]
        except IndexError:
            area[2] = ''
        print area
        second_driver = webdriver.Firefox()
        surl = base+rlink[0]    
        second_driver.get(surl)

        second_parser = html.fromstring(second_driver.page_source,second_driver.current_url)
        
        setFields(udate,surl,area,second_parser,c,conn)
         
        second_driver.close()
    sp = randint(9,17)
    time.sleep(sp)
    #.//*[@id='pagination']/a[4]
    #xpage = '//*[@id="pagination"]/a['+str(i+2)+']/@href'
    #rpage = parser.xpath(xpage)
    #print i,'next page',rpage[0]    
   
    #driver.get(base+rpage[0])

    #elem = driver.find_element_by_class("nextPage")
    driver.find_element_by_xpath(".//*[@id='pagination']/a[16]").click()
    sp = randint(8,16)
    time.sleep(sp)
    parser = html.fromstring(driver.page_source,driver.current_url)
driver.close()
#conn.commit()
conn.close()
