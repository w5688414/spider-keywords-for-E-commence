
from appium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

cap={
  "platformName": "Android",
  "platformVersion": "6.0.1",
  "deviceName": "emulator-5554",
  "appPackage": "com.xunmeng.pinduoduo",
  "appActivity": "com.xunmeng.pinduoduo.ui.activity.MainFrameActivity",
  "noReset": True
}
driver =webdriver.Remote("http://localhost:4723/wd/hub",cap)
def getSize():
    x=driver.get_window_size()['width']
    y=driver.get_window_size()['height']
    return (x,y)

position=getSize()

x1=int(position[0]*0.5)
y1=int(position[1]*0.75)
y2=int(position[1]*0.25)

car_list=[]

#向下滑动
def swipe_down(driver,t=500,n=1):
    s = driver.get_window_size()
    x1 = s['width'] * 0.5  # x坐标
    y1 = s['height'] * 0.25 # 起点y坐标
    y2 = s['height'] * 0.75 # 终点y坐标
    for i in range(n):
        driver.swipe(x1,y1,x1,y2,t)

def swipeUp(driver,t=500,n=1):
    """向上屏幕滑动"""
    size = driver.get_window_size()
    x1 = size["width"] * 0.5 # x坐标
    y1 = size["height"] * 0.75 # 起点 y坐标
    y2 = size["height"] * 0.25 # 终点 y 坐标
    for i in range(n):
        driver.swipe(x1,y1,x1,y2,t)

def search_by_keyword(driver,key_word):
    
    el5 = driver.find_element_by_id("com.xunmeng.pinduoduo:id/co0")
    el5.send_keys(key_word)
    el6 = driver.find_element_by_id("com.xunmeng.pinduoduo:id/cno")
    el6.click()
    try:
        time.sleep(3)
        el7 = driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout[3]/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.widget.TextView")
        el7.click()
    except Exception as e:
        pass

    time.sleep(3)
    while(True):
        try:
            swipeUp(driver)
            time.sleep(3)
            el7=driver.find_element_by_id('com.xunmeng.pinduoduo:id/a9b')
            driver.back()
            break
        except Exception as e:
            print(e)
            


if(WebDriverWait(driver,10).until(lambda x:x.find_element_by_id("com.xunmeng.pinduoduo:id/yl"))):
    list_keyword=['iphone','大米']
    el4 = driver.find_element_by_id("com.xunmeng.pinduoduo:id/yl")
    el4.click()
    time.sleep(3)
    for item in list_keyword:
        search_by_keyword(driver,item)
    # el4 = driver.find_element_by_id("com.xunmeng.pinduoduo:id/byx")
    # el4.click()
    # time.sleep(3)
    # el5 = driver.find_element_by_id("com.xunmeng.pinduoduo:id/bz3")
    # el5.send_keys("iphone")
    # el6 = driver.find_element_by_id("com.xunmeng.pinduoduo:id/bys")
    # el6.click()
    # try:
    #     time.sleep(3)
    #     el7 = driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout[3]/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.widget.TextView")
    #     el7.click()
    # except Exception as e:
    #     pass

    # time.sleep(3)
    
    # while(True):
    #     try:
    #         swipeUp(driver)
    #         time.sleep(3)
    #         el7=driver.find_element_by_id('com.xunmeng.pinduoduo:id/a9b')
    #         driver.back()
    #         break
    #     except Exception as e:
    #         print(e)
            
    


# if(WebDriverWait(driver,3).until(lambda x:x.find_element_by_id("com.maihaoche.bentley:id/iv_first"))):
#     while(True):
#         try:
#             driver.swipe(x1,y1,x1,y2)
#         except Exception as e:
#             print(e)
#             pass
#         try:
#             # title=driver.find_elements_by_class_name("android.widget.LinearLayout")[0].click()
#             # title=driver.find_elements_by_xpath("//android.widget.TextView[@resource-id='com.maihaoche.bentley:id/tv_title']")
#             title=driver.find_element_by_id("com.maihaoche.bentley:id/tv_title")
#             # title=driver.find_element_by_id("com.maihaoche.bentley:id/tv_properties")
#             car=title.text
#             if(car not in car_list):
#                 car_list.append(car)
#                 print(car)
#                 title.click()
        
            
#             # title=driver.find_elements_by_xpath("//android.view.ViewGroup[@resource-id='com.maihaoche.bentley:id/recycler_main']/android.widget.LinearLayout[3]")
#             # break
            
#         except Exception as e:
#             print(e)
#             pass
#         try:
#             el2 = driver.find_element_by_id("com.maihaoche.bentley:id/left_btn")
#             # print(el2.text)
#             el2.click()

#         except Exception as e:
#             print(e)
#             pass

#         time.sleep(1)
