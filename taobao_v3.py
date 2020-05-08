from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from pyquery import  PyQuery as pq
import os
import re
import random


def search(driver,KEYWORD,index,login_flag):
    url='https://s.taobao.com/search?q={}&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&s={}'.format(KEYWORD,index*44)
    driver.get(url)
    if(login_flag):
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="login"]/div[1]/i').click()
        time.sleep(10)

    sec=random.randint(2,10)
    time.sleep(sec)
    # time.sleep(15)
    list_data=get_products()

    return list_data

# 解析方法
def get_products():

    # 通过page_source方法获取源代码
    html = driver.page_source
    currentPageUrl = driver.current_url
    print("当前页面的url是：", currentPageUrl)
    # 初始化pyquery对象
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    list_data=[]
    for item in items:
        product=[]
        # print(item)
        image="https:"+item.find('.pic .img').attr('src')
        # print(image)
        # print(item.find('.pic').find('a').attr('href'))
        url="https:"+item.find('.pic').find('a').attr('href')
        # print(url)
        price=item.find('.price').text().strip()[2:]
        deal=item.find('.deal-cnt').text()[:-3]

        title=item.find('.title').text()
        shop=item.find('.shop').text()
        location=item.find('.location').text()

        flag=False
        
        if('+' in deal):
            deal_num=deal[:-1]
        else:
            deal_num=deal

        if('万' in deal_num):
            flag=True
        elif(int(deal_num)>=20):
            flag=True
        else:
            return list_data

        if(flag):
            product=[shop,title,price,deal,url,image,location]
            list_data.append(product)
        
    return list_data

def output_to_csv(list_data,csv_name):
    column_name = ['shop', 'title','price','deal','url',"image",'location']
    xml_df = pd.DataFrame(list_data, columns=column_name)
    print(xml_df.shape)
    xml_df=xml_df.drop_duplicates()
    print(xml_df.shape)
    xml_df.to_csv(csv_name, index=None)

def get_total_page(driver,KEYWORD):
    
    url='https://s.taobao.com/search?q={}&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&s={}'.format(KEYWORD,44)
    driver.get(url)
    time.sleep(2)
    try:
        wait = WebDriverWait(driver,40)
        driver.find_element_by_xpath('//*[@id="login"]/div[1]/i').click()
    except Exception as e:
        print(e)
        pass
    time.sleep(10)
    total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
    print('total page '+total.text)
    page_total = total.text.replace("共","").replace("页","").replace("，","")
    return page_total


def search_by_keyword_v1(driver,root_path,KEYWORD):

    csv_name=os.path.join(root_path,KEYWORD+'.csv')
    if(os.path.exists(csv_name)):
        return
    list_res=[]
    page_num=get_total_page(driver,KEYWORD)
    login_flag=False
    for i in range(0,int(page_num),1):
        print('下载第{}'.format(i))
        list_data=search(driver,KEYWORD,i,login_flag)
        if(not list_data):
            break
        list_res+=list_data
    output_to_csv(list_res,csv_name)


if __name__ == '__main__':
    driver = webdriver.Chrome()
    list_keys=['荣事达煮茶器','荣事达养生壶','荣事达电饭煲','富安娜','富安娜四件套','富安娜床上用品','富安娜床单','富安娜被套']
    root_path='taobao'
    
    for key in list_keys:
        print('当前关键字:{}'.format(key))
        search_by_keyword_v1(driver,root_path,key)
    driver.close()