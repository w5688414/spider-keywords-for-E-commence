from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from pyquery import PyQuery as pq
import pandas as pd
import os
# app = QApplication([])
# view = QWebEngineView()

# view.load(QUrl("https://www.tmall.com/"))
# view.show()
# app.exec_()

from PyQt5.Qt import *
import sys

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUI()


    def setupUI(self):
        self.mHtml = ""
        layout = QVBoxLayout()
        self.web_browser = QWebEngineView()
        # self.web_browser.load(QUrl('https://pan.baidu.com/s/17XlMuMzfQhwJ5R1Bn7yuiA#list/path=%2F'))
        btn = QPushButton('加载脚本')
        layout.addWidget(btn)
        layout.addWidget(self.web_browser)
        self.setLayout(layout)
        self.web_browser.load(QUrl('https://www.tmall.com/'))
        btn.clicked.connect(self.add_script)
        self.dict_data={}
        # self.web_browser.loadFinished.connect(self.add_script)

    def callback(self, html):
        self.mHtml = html
        # self.htmlFinished.emit()
        # print(self.mHtml)
        # pq模块解析网页源代码
        doc = pq(html)
        keywords=doc('#mq').attr('value')
        print(keywords)
        if(keywords in self.dict_data):
            list_data=self.dict_data[keywords]
        else:
            list_data=[]
         # 存储天猫商品数据
        good_items = doc('#J_ItemList .product').items()
        # 遍历该页的所有商品
        for item in good_items:
            products=[]
            good_title = item.find('.productTitle').text().replace('\n',"").replace('\r',"")
            good_status = item.find('.productStatus').find('em').text().replace(" ","").replace("笔","").replace('\n',"").replace('\r',"")
            good_price = item.find('.productPrice').text().replace("¥", "").replace(" ", "").replace('\n', "").replace('\r', "")
            good_url = item.find('.productImg').attr('href')
                # print(good_title + "   " + good_status + "   " + good_price + "   " + good_url + '\n')
            products=[good_title,good_status,good_price,good_url]
            list_data.append(products)
        csv_name=os.path.join('TM',keywords+'.csv')
        output_to_csv(list_data,csv_name)
        self.dict_data[keywords]=list_data
        with open('test.html','w') as f:
            f.write(self.mHtml)

    def add_script(self):
        print('按钮已被点击')
        res=self.web_browser.page().toHtml(self.callback)
        # print(res)

def output_to_csv(list_data,csv_name):
    column_name = ['good_title', 'good_status','good_price','good_url']
    xml_df = pd.DataFrame(list_data, columns=column_name)
    print(xml_df.shape)
    xml_df=xml_df.drop_duplicates()
    print(xml_df.shape)
    xml_df.to_csv(csv_name, index=None)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

