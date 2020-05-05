from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import time
import pandas as pd
import urllib.parse
import os

browser = webdriver.Chrome()
wait = WebDriverWait(browser,20)

def get_url_encode(key,value):
    values={}
    values[key]=value
    KEYWORD=urllib.parse.urlencode(values)
    return KEYWORD


#京东上搜索关键词，发起请求
def get_KEYWORD(KEYWORD):
    print('正在狗东搜索关键词...当前关键词：'+KEYWORD)
    try:
        # browser.get('https://www.jd.com')
        # input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#key')))
        # submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#search > div > div.form > button')))
        # input.send_keys(KEYWORD)
        # submit.click()
        
        # KEYWORD=get_url_encode('keyword',KEYWORD)
        # wq=get_url_encode('keyword',KEYWORD)
        url='https://search.jd.com/Search?keyword={}&enc=utf-8&wq={}&psort=4'.format(KEYWORD,KEYWORD)
        print(url)
        # url="https://search.jd.com/Search?{}&qrst=1&psort=4&psort=4&click=2".format(KEYWORD,wq)
        browser.get(url)
        pagenumber = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > em:nth-child(1) > b'))).text
        print(pagenumber)
        get_product_info()
        if(pagenumber):
            return int(pagenumber)
        else:
            return 1
    except TimeoutException as e:
        print(e)
        return 1
        # return get_KEYWORD(KEYWORD)
#实现翻页功能
def get_next_page(pagenumber):
    print('-------------正在获取第'+str(pagenumber)+'页..-----------------')
    try:
        if(pagenumber==1):
            list_goods=get_product_info()
            return list_goods
        js = "window.scrollTo(972,503)"
        browser.execute_script(js)      #---------解决元素可定位却不可用。报错：...is not clickable ...
        next = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_topPage > a.fp-next')))

        next.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#J_topPage > span > b'),str(pagenumber)))
        list_goods=get_product_info()
        return list_goods
    except TimeoutException as e:
        print(e)
        get_next_page(pagenumber)
#获取商品信息
def get_product_info():
    time.sleep(1)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.w .container .g-main2 .m-list .ml-wrap .goods-list-v2 .clearfix .gl-item'))
    )
    html = browser.page_source
    doc = pq(html)
    goods = doc('.w .container .g-main2 .m-list .ml-wrap .goods-list-v2 .clearfix .gl-item').items()
    list_goods=[]
    for good in goods:
        # print(good)
        link_and_img = pq(good.find('.gl-i-wrap .p-img').html())

        good_link='https:'+str(link_and_img.find('a').attr('href'))
        good_img='https:'+str(link_and_img.find('img').attr('src'))

        good_price=good.find('.gl-i-wrap .p-price').text()
        good_name=good.find('.gl-i-wrap .p-name').text()
        good_comment=good.find('.gl-i-wrap .p-commit').text()
        good_shop=good.find('.gl-i-wrap .p-shop').text()
        # product = {
        #     'good_link':'https:'+str(link_and_img.find('a').attr('href')),
        #     'good_img' : 'https:'+str(link_and_img.find('img').attr('data-lazy-img')),
        #     'good_price': good.find('.gl-i-wrap .p-price').text(),
        #     'good_name' : good.find('.gl-i-wrap .p-name').text(),
        #     'good_commit' : good.find('.gl-i-wrap .p-commit').text(),
        #     'good_shop' : good.find('.gl-i-wrap .p-shop').text()
        # }
        # if product['good_img'] == 'done':
        #     product['good_img'] = 'https:'+str(link_and_img.find('img').attr('src'))
        if('+' in good_comment):
            comment_num=good_comment[:-4]
        else:
            comment_num=good_comment[:-3]
        flag=False
        if('万' in comment_num):
            flag=True
        elif(int(comment_num)>=10):
            flag=True
        else:
            return list_goods
        if(flag):
            # print(comment_num)
            # print(good_commit)
            list_goods.append([good_shop,good_name,good_price,good_comment,good_link,good_img])
        # save_2_mongo(product)
    return list_goods

def output_to_csv(list_data,csv_name):
    column_name = ['good_shop', 'good_name','good_price','comment_num',"good_link",'good_img']
    xml_df = pd.DataFrame(list_data, columns=column_name)
    print(xml_df.shape)
    xml_df=xml_df.drop_duplicates()
    print(xml_df.shape)
    xml_df.to_csv(csv_name, index=None)

def crawdata(KEYWORD,root_path):
    try:
        csv_name=os.path.join(root_path,KEYWORD+'.csv')
        if(os.path.exists(csv_name)):
            return
        pagenum = get_KEYWORD(KEYWORD)
        all_goods=[]
        
        for i in range(1,pagenum+1):
            list_goods=get_next_page(i)
            all_goods+=list_goods
            if(not list_goods):
                break
            # break
        
        output_to_csv(all_goods,csv_name)
    except Exception as e:
        print(e)
        print('某些位置出错了..')
    # finally:
    #     browser.close()


def main():
    root_path='JD'
    # KEYWORD = '珀利'
    # df=pd.read_excel('keywords.xlsx')
    list_keys=['珀利','VIVO充电器','魅族充电器','平安承保','荣事达煮茶器','荣事达养生壶','荣事达电饭煲']
    for item in list_keys:
        crawdata(item,root_path)
    browser.close()

if __name__ == '__main__':
    main()