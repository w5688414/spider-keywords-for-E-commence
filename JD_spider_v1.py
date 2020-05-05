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

        # KEYWORD=get_url_encode('keyword',KEYWORD)
        # wq=get_url_encode('keyword',KEYWORD)
        # https://search.jd.com/Search?keyword=%E7%BA%A2%E6%98%9F%E7%85%A7%E8%80%80%E4%B8%AD%E5%9B%BD%20%E9%95%BF%E6%B1%9F%E6%96%87%E8%89%BA%E5%87%BA%E7%89%88%E7%A4%BE&qrst=1&wq=%E7%BA%A2%E6%98%9F%E7%85%A7%E8%80%80%E4%B8%AD%E5%9B%BD%20%E9%95%BF%E6%B1%9F%E6%96%87%E8%89%BA%E5%87%BA%E7%89%88%E7%A4%BE&ev=publishers_%E9%95%BF%E6%B1%9F%E6%96%87%E8%89%BA%E5%87%BA%E7%89%88%E7%A4%BE%5E&psort=4&click=0
        url='https://search.jd.com/Search?keyword={}&enc=utf-8&wq={}&psort=4&ev=publishers_长江文艺出版社'.format(KEYWORD,KEYWORD)
        print(url)
        browser.get(url)
        pagenumber = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > em:nth-child(1) > b'))).text
        print(pagenumber)
        # get_product_info()
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
        return None
        # get_next_page(pagenumber)


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
        
        link_and_img = pq(good.find('.gl-i-wrap .p-img').html())
        # print(link_and_img)

        good_link='https:'+str(link_and_img.find('a').attr('href'))
        good_img='https:'+str(link_and_img.find('img').attr('src'))

        good_price=good.find('.gl-i-wrap .p-price').text()
        good_name=good.find('.gl-i-wrap .p-name').text()
        good_comment=good.find('.gl-i-wrap .p-commit').text()
        good_shop=good.find('.gl-i-wrap .p-shop').text()
    

        if('+' in good_comment):
            comment_num=good_comment[:-4]
        else:
            comment_num=good_comment[:-3]
        flag=False
        if('万' in comment_num):
            flag=True
        elif(int(comment_num)>=20):
            flag=True
        else:
            return list_goods
        if(flag):
            res=[good_shop,good_name,good_price,good_comment,good_link,good_img]
            print(res)
            list_goods.append(res)
        
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
            print('page '+str(i))
            list_goods=get_next_page(i)
            all_goods+=list_goods
            if(not list_goods):
                break
            # break
        
        output_to_csv(all_goods,csv_name)
    except Exception as e:
        print(e)
        print('某些位置出错了..')



def main():
    root_path='JD'
    # KEYWORD = '珀利'
    # df=pd.read_excel('keywords.xlsx')
    list_keys=['寂静的春天','昆虫记','星星离我们有多远','红星照耀中国',
    '孤独的小螃蟹','小狗的小房子','歪脑袋木头桩','小鲤鱼跳龙门','一只想飞的猫']
    for item in list_keys:
        crawdata(item,root_path)
    browser.close()

if __name__ == '__main__':
    main()