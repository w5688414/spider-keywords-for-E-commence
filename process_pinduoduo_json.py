import json
import pandas as pd
import os
import glob


def read_json(json_path):
    with open(json_path,'r') as load_f:
        load_dict = json.load(load_f)
    return load_dict


def output_to_csv(list_data,csv_name):
    column_name = ['mallName', 'goodsName','salesTip','price','goods_url',"image"]
    xml_df = pd.DataFrame(list_data, columns=column_name)
    print(xml_df.shape)
    xml_df=xml_df.drop_duplicates()
    print(xml_df.shape)
    xml_df.to_csv(csv_name, index=None)

def parse_data(list_data):
    list_res=[]
    for item in list_data:
        product=[]
        mallName=item['mallName']
        goodsName=item['goodsName']
    #     goodsDesc=item['goodsDesc']
        
        salesTip=item['salesTip']
        goods_url='https://youhui.pinduoduo.com/goods/goods-detail?goodsId='+str(item['goodsId'])
        image=item['goodsImageUrl']
        price=(item['minGroupPrice']-item['couponMinOrderAmount'])/1000
        
        product=[mallName,goodsName,salesTip,price,
                goods_url,image]
        list_res.append(product)
    return list_res

def process(filter_path,index):
    list_data=[]
    for name in glob.glob(filter_path):
        print (name)
        # json_path='./pinduoduo_raw/1.json'
        load_dict=read_json(name)
        data=load_dict['result']['goodsList']
        list_res=parse_data(data)
        list_data+=list_res

    csv_name=os.path.join('pinduoduo',str(index)+'.csv')
    output_to_csv(list_data,csv_name)     



if __name__ == "__main__":
    root_path='./pinduoduo_raw'

    for i in range(1,17,1):
        key=str(i)+'_*'
        filter_path=os.path.join(root_path,key)
        process(filter_path,i)