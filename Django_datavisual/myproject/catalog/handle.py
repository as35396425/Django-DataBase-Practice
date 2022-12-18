
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


def Sex_Survived(data):
    
    survived = [int(x) for x in data['Survived']]
    Sex= [str(x) for x in data['Sex']]
    sur_male = 0
    sur_female = 0
    non_sur_male = 0
    non_sur_female = 0    
    for i,j in zip(Sex,survived):
        if j == 1:
            if i =='male':
                sur_male += 1
            if i =='female':
                sur_female += 1
        if j ==0:
            if i =='male':
                non_sur_male += 1
            if i =='female':
                non_sur_female += 1
    return[[non_sur_male,non_sur_female],[sur_male,sur_female] ]
    

        
def Pclass_Sur(data):
    pclass = [int(x) for x in data['Pclass']]
    survived = [int(x) for x in data['Survived']]

    sur_1 = 0
    sur_2 = 0
    sur_3 = 0
    non_sur_1 = 0
    non_sur_2 = 0
    non_sur_3 = 0
    for i,j in zip(pclass,survived):
        if j == 1:
            if i ==1:
                sur_1 += 1
            elif i ==2:
                sur_2 += 1
            elif i ==3:
                sur_3 += 1
    
        if j ==0:
            if i ==1:
                non_sur_1 += 1
            elif i ==2:
                non_sur_2 += 1
            elif i ==3:
                non_sur_3 += 1
                
    return[[non_sur_1,non_sur_2,non_sur_3],[sur_1,sur_2,sur_3]]


def Emb_Survived(data):
    
    survived = [int(x) for x in data['Survived']]
    embarked= [str(x) for x in data['Embarked']]
    sur_S = 0
    sur_C = 0
    sur_Q = 0
    non_sur_S = 0
    non_sur_C = 0
    non_sur_Q = 0
    for i,j in zip(embarked,survived):
        if j == 1:
            if i =='S':
                sur_S += 1
            elif i =='C':
                sur_C += 1
            elif i =='Q':
                sur_Q += 1
    
        if j ==0:
            if i =='S':
                non_sur_S += 1
            elif i =='C':
                non_sur_C += 1
            elif i =='Q':
                non_sur_Q += 1
                
    return[[non_sur_S,non_sur_C,non_sur_Q],[sur_S,sur_C,sur_Q]]

def survived(data):
    survived = [int(x) for x in data['Survived']]

    return [(survived.count(0)),(survived.count(1))]



def price(page,name):
    cou = 1
    keywordList=[]

    catch_page = int(page)

    for i in range(cou):
        keywordList.append(name)


    for keyword in keywordList:
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

            if r.status_code == requests.codes.ok:
                data = r.json()
                infom = ""
                D=dict()
                for i in range(len(data["items"])):

                    name = data["items"][i]["item_basic"]["name"]
                    print(name)
                    price = int(data["items"][i]["item_basic"]["price"]) // 100000  
                    #print("{}:{}".format(name,price))
                    item_id = data["items"][i]["item_basic"]["itemid"]
                    shop_id = data["items"][i]["item_basic"]["shopid"]
                    id_url = f'https://shopee.tw/product/{shop_id}/{item_id}'        
                    outP ="{}:{}".format(name,price)
                    #if 40000 > price > 10000:  #考慮到賣家會不合理設價格，先設此if條件
                    infom+=outP+'\n'
                    D[name] = price
                    name.replace(",","")
                    name_list.append(name)
                    price_list.append(price)
                    url_list.append(id_url)
                    print(id_url)
                print(url_list)

            else:
                print("error")
                break


            #print(D)
            data_P = pandas.Series(D,dtype = 'float64')

            data_pandas_frame = pandas.DataFrame( {"name":name_list
                                                , "price":price_list  
                                                                        } )



        Pdata = numpy.array(data_pandas_frame['price'])  #做成NP

        uliprice = []
        uliname = []

        for i in range(len(price_list)):
            if  price_list[i] :
                uliprice.append(price_list[i])
                uliname.append(name_list[i])



        
        xpt = range(len(uliprice))
        ypt = uliprice

        data_pandas_frame = pandas.DataFrame( {  "name":uliname
                                                , "price":uliprice  })
        

        
    return [uliname,uliprice,url_list]




#======
def partition(arr,low,high): 
    i = ( low-1 )         
    pivot = arr[high]     
  
    for j in range(low , high): 
  
        if   arr[j] <= pivot: 
          
            i = i+1 
            arr[i],arr[j] = arr[j],arr[i]
    arr[i+1],arr[high] = arr[high],arr[i+1] 
    
    return ( i+1 ) 
  
 

def quickSort(arr,low,high): 
    if low < high: 
        print(arr,low,high)

        pi = partition(arr,low,high) 
  
        quickSort(arr, low, pi-1) 
        quickSort(arr, pi+1, high) 
  





def price_test(page,name):
    
    cou = 1
    keywordList=[]
    #catch_page = int(input())
    catch_page = int(page)
    
    for i in range(cou):
        keywordList.append(name)
        
        
    for keyword in keywordList:
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
                    
                    print(id_url)
                    
                print(url_list)

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
            if  lowlim<=price_list[i]<=uplim :
    
                uliprice.append(price_list[i])
                uliname.append(name_list[i])
                uliurl.append(url_list[i])
    #print(lowlim,uplim,IQR)
    print(uplim)

        
    return [uliname,uliprice,uliurl]


def auto_get():
    p_name = ["gtx1050","gtx1060","gtx1070","gtx1080,gtx1650,gtx1660,rtx2070,rtx2080"]
    #p_name = ["gtx1050"]
    
    
    
    #print(result[0][1])

    
    conn = sqlite3.connect(r"C:\Users\wow35\OneDrive\桌面\Django_datavisual\myproject\db.sqlite3") 
    cursor = conn.cursor()
    sql = "INSERT INTO catalog_price(cName, cPrice,cUrl,pName_id_id,web_record)VALUES(? ,? ,? ,?,?)"
    del_repeat = "DELETE FROM catalog_price WHERE id NOT IN(SELECT MAX(id) FROM catalog_price GROUP BY cPrice)"
    #刪掉不是最大的ID(最大ID代表最新)
    
    c=0
    for pname in p_name:
        shp_result = price_test(1,pname)
        lut_result = get_lutan(1,pname)
        c+=1 
        for i in range(len(shp_result[0])):
            cursor.execute(sql, (shp_result[0][i],shp_result[1][i],shp_result[2][i],c,"蝦皮"))
        for i in range(len(lut_result[0])):
            cursor.execute(sql, (lut_result[0][i],lut_result[1][i],lut_result[2][i],c,"露天"))
        cursor.execute(del_repeat)
        conn.commit()



def select_gpu(choice):
    cPrice_l = []
    conn = sqlite3.connect(r"C:\Users\wow35\OneDrive\桌面\Django_datavisual\myproject\db.sqlite3") 
    cursor = conn.cursor()
    sp_price=[]
    lut_price =[]
    select_data = "SELECT pName_id_id,cPrice,web_record FROM catalog_price ORDER BY cPrice"

    rows = cursor.execute(select_data)
    for row in rows:
        if row[0] == int(choice):
            cPrice_l.append(int(row[1]))
            if row[2] == "蝦皮":
                sp_price.append(int(row[1]))#加入蝦皮抓到的
            if row[2] == "露天":
                lut_price.append(int(row[1]))
        if choice == "-1":
            cPrice_l.append(int(row[1]))
            if row[2] == "蝦皮":
                sp_price.append(int(row[1]))#加入蝦皮抓到的
            if row[2] == "露天":
                lut_price.append(int(row[1]))
    
    rows.close()
    return  [cPrice_l,sp_price,lut_price]

#auto_get()



def get_lutan(pages,keywd):
# 商品分類
    cateid = '00110005'#電腦零組件  #'00110005'
    

    prodids = []   #紀錄商品ID
    name_list  = []
    price_list = []
    url_list=[]


    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
                    'x-api-source': 'pc'}

    for page in list(range(0, pages)):
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
        if lowlim<=price_list[i]<=uplim :
            uliprice.append(price_list[i])
            uliname.append(name_list[i])
            uliurl.append(url_list[i])
    
    
    return [uliname,uliprice,uliurl]


