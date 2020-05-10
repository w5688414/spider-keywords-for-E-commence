from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from pyquery import  PyQuery as pq
import os
import re



def login(KEYWORD,login_flag):
    driver.find_element_by_xpath('//*[@id="q"]').send_keys(KEYWORD)
    driver.find_element_by_xpath('//*[@id="J_TSearchForm"]/div[1]/button').click()
    if(login_flag):
        driver.find_element_by_xpath('//*[@id="login"]/div[1]/i').click()

    # 扫码登录
    print('扫码登陆')
    time.sleep(15)
    wait = WebDriverWait(driver,40)
    deal=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#J_relative > div.sort-row > div > ul > li:nth-child(2) > a")))
    deal.click()
    total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
    return total.text
    #J_relative > div.sort-row > div > ul > li:nth-child(2) > a

def get_page_number(KEYWORD):
    driver.find_element_by_xpath('//*[@id="q"]').send_keys(KEYWORD)
    driver.find_element_by_xpath('//*[@id="J_TSearchForm"]/div[1]/button').click()
    time.sleep(10)
    wait = WebDriverWait(driver,40)
    deal=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#J_relative > div.sort-row > div > ul > li:nth-child(2) > a")))
    deal.click()
    total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
    return total.text


# 滑动滑条，加载全部信息
def drop_down():
    for x in range(1, 11, 2):
        time.sleep(0.5)# 防止被预测到反爬
        h = x/10
        js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % h
        driver.execute_script(js)


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
        
        # print(product)
        # print(deal)
        flag=False
        
        if('+' in deal):
            deal_num=deal[:-1]
        else:
            deal_num=deal

        if('万' in deal_num):
            flag=True
        elif(int(deal_num)>=50):
            flag=True
        else:
            return list_data
  
        if(flag):
            product=[shop,title,price,deal,url,image,location]
            list_data.append(product)
    return list_data

def next_page(page_number):
    wait = WebDriverWait(driver,40)
    input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))
        )
    submit = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
    input.clear()
    input.send_keys(page_number)
    submit.click()



def output_to_csv(list_data,csv_name):
    column_name = ['shop', 'title','price','deal','url',"image",'location']
    xml_df = pd.DataFrame(list_data, columns=column_name)
    print(xml_df.shape)
    xml_df=xml_df.drop_duplicates()
    print(xml_df.shape)
    xml_df.to_csv(csv_name, index=None)

def search_by_keyword(KEYWORD,root_path,driver,login_flag):
    print(KEYWORD)
    try:
        csv_name=os.path.join(root_path,KEYWORD+'.csv')
        if(os.path.exists(csv_name)):
                return
        list_res=[]
        driver.get('https://www.taobao.com/')
        total =login(KEYWORD,login_flag)
        drop_down()
        total = int(re.compile('(\d+)').search(total).group(1))
        print('total page '+str(total))
        for i in range(1, total):
            print('download page '+str(i))
            list_data=get_products()
            if(list_data):
                list_res+=list_data            
                time.sleep(2)
                drop_down()
                print('next....')
                next_page(page_number=i+1)
            else:
                break
        output_to_csv(list_res,csv_name)
    except Exception as e:
        # output_to_csv(list_res,csv_name)
        print(e)
        print('某些位置出错了..')






if __name__ == '__main__':
    driver = webdriver.Chrome()
    root_path='taobao'
    list_keys=['珀利','VIVO充电器','魅族充电器','平安承保','荣事达煮茶器','荣事达养生壶','荣事达电饭煲']
    book_keys=['寂静的春天','昆虫记','星星离我们有多远','红星照耀中国',
    '孤独的小螃蟹','小狗的小房子','歪脑袋木头桩','小鲤鱼跳龙门','一只想飞的猫']
    book_keys=[item+' 长江文艺出版社' for item in book_keys ]
    list_keys+=book_keys
    login_flag=True
    for item in list_keys:
        csv_name=os.path.join(root_path,item+'.csv')
        if(os.path.exists(csv_name)):
            continue
        if(login_flag):
            search_by_keyword(item,root_path,driver,login_flag)
            login_flag=False
        else:
            search_by_keyword(item,root_path,driver,login_flag)
    driver.close()
