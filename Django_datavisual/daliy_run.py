
import re
import pandas as pd 
import numpy as np
import sqlite3

import numpy
import requests
import urllib
from bs4 import BeautifulSoup
import pandas

import re
import json
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random

def price_test(page,name):
    cou = 1
    keywordList=[]

    #catch_page = int(input())
    catch_page = int(page)



    keyword = name


    
    name_list  = []
    price_list = []
    url_list=[]
    for page in range(1,catch_page+1):
        headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
                'x-api-source': 'pc',
                'referer': f'https://shopee.tw/search?keyword={urllib.parse.quote(keyword)}',
            } 


        s = requests.Session()

            
            
        base_url = 'https://shopee.tw/api/v4/search/search_items/' #基本頁面  網址若v2 name在items裡面  若v4 name在 items的item_basic裡面

        query = f"by=filters=9&facet=11041538&relevancy&keyword={keyword}&limit=5&newest=0&order=desc&page_type=search&version=2&page={page}"  #不同的值給予不同類型頁面 ex: limit = 10 order=desc
            #categoryids=7904 分類顯示卡
        url = base_url + '?' + query   #製作url
        r = s.get(url, headers=headers) 
            


        print(url)
        if r.status_code == requests.codes.ok:
            data = r.json()
            infom = ""

            for i in range(len(data["items"])):

                name = data["items"][i]["item_basic"]["name"]
                price = int(data["items"][i]["item_basic"]["price"]) // 100000  
                item_id = data["items"][i]["item_basic"]["itemid"]
                shop_id = data["items"][i]["item_basic"]["shopid"]
                id_url = f'https://shopee.tw/product/{shop_id}/{item_id}'        
                outP ="{}:{}".format(name,price)
                infom+=outP+'\n'
                name.replace(",","")
                name_list.append(name)
                price_list.append(price)
                url_list.append(id_url)
                #print(id_url)
            #print(url_list)

        else:
            print("error")
            break



        data_pandas_frame = pandas.DataFrame( {"name":name_list
                                                , "price":price_list  
                                                                        } )





    price_Info = data_pandas_frame['price'].describe()

    IQR = price_Info["75%"]-price_Info["25%"]
    uplim =  price_Info["75%"]+1.5*IQR
        #lowlim = price_Info["25%"]-1*IQR
    lowlim = 500
        
    uliprice = []
    uliname = []
    uliurl = []
    for i in range(len(price_list)):
        if  lowlim<price_list[i]<uplim :
    
            uliprice.append(price_list[i])
            uliname.append(name_list[i])
            uliurl.append(url_list[i])
    #print(lowlim,uplim,IQR)
    print(uplim)

        
    return [uliname,uliprice,uliurl]


def auto_get(page):
    p_name = ["gtx1050","gtx1060","gtx1070","gtx1080","gtx1650","gtx1660","rtx2060","rtx2070","rtx2080"]
    #p_name = ["gtx1050"]
    
    #print(result[0][1])

    
    conn = sqlite3.connect(r"C:\Users\wow35\OneDrive\桌面\Django_datavisual\myproject\db.sqlite3") 
    cursor = conn.cursor()
    sql = "INSERT INTO catalog_price(cName, cPrice,cUrl,pName_id_id,web_record)VALUES(? ,? ,? ,? ,? )"
    del_repeat = "DELETE FROM catalog_price WHERE id NOT IN(SELECT MAX(id) FROM catalog_price GROUP BY cUrl)"
    #刪掉不是最大的ID(最大ID代表最新)
    #datetime_str = datetime.now()

    c=0
    for pname in p_name:
        shp_result = price_test(page,pname)
        lut_result = get_lutan(page,pname)
        c+=1 
        for i in range(len(shp_result[0])):
            cursor.execute(sql, (shp_result[0][i],shp_result[1][i],shp_result[2][i],c,"蝦皮"))
        for i in range(len(lut_result[0])):
            cursor.execute(sql, (lut_result[0][i],lut_result[1][i],lut_result[2][i],c,"露天"))
        cursor.execute(del_repeat)
        conn.commit()


def get_lutan(pages,keywd):
# 商品分類
    cateid = '00110005'#電腦零組件  #'00110005'
    

    prodids = []   #紀錄商品ID
    name_list  = []
    price_list = []
    url_list=[]


    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
                    'x-api-source': 'pc'}

    for page in list(range(0, pages)):#接API 開始抓row 以頁數做for
        offset = 1 + 80*page#從第幾結果開始
        url = f'https://rtapi.ruten.com.tw/api/search/v3/index.php/core/prod?cateid={cateid}&sort=rnk%2Fdc&offset={offset}&limit=80&2653512&_callback=jsonpcb_CoreProd&q={keywd}&isnew=0&location=tw'
        s= requests.Session()
        resp = s.get(url, headers=headers)
            
        data = re.sub(r'try\{jsonpcb_CoreProd\(|\);\}catch\(e\)\{if\(window.console\)\{console.log\(e\);\}\}','', resp.text)
        #print(data)        
        for prod in json.loads(data)['Rows']:#開始讀Rows 且把商品ID加進list
            prodids.append(prod['Id'])
        prodids = list(set(prodids))
        print('There are {} prods in list.'.format(len(prodids)))
            
            
    for i, prodid in enumerate(prodids):

        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
                    'x-api-source': 'pc'}
        url = 'https://goods.ruten.com.tw/item/show?' + prodid  #依照商品ID列表，連到商品頁面用BS4抓資料
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text)#features="lxml"
        data1 = json.loads(soup.find('script',{'type':'application/ld+json'}).text)




        name_list.append(data1["name"])
        price_list .append(int(data1['offers']['price']))
        url_list.append(data1["offers"]["url"])
        #print(type(data1['offers']['price']))
        time.sleep(random.randint(0,2))
        print("handle {} now".format(url))  
    df = pandas.DataFrame( {"price":price_list} )
    price_Info = df["price"].describe()
    print(price_Info)
    IQR = price_Info["75%"]-price_Info["25%"]
    uplim =  price_Info["75%"]+1.5*IQR
    lowlim = 500
    uliprice = []
    uliname = []
    uliurl = []
    for i in range(len(price_list)):
        if lowlim<price_list[i]<uplim :
            uliprice.append(price_list[i])
            uliname.append(name_list[i])
            uliurl.append(url_list[i])
    
    
    return [uliname,uliprice,uliurl]


auto_get(20)

#datetime_str = datetime.now()
#print(datetime_str)
