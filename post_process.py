import  pandas  as pd
import random
import os


def convert(csv_name,excel_name):
    df=pd.read_csv(csv_name)
    df.to_excel(excel_name,index=None)

def create_root(path):
    os.makedirs(path,exist_ok=True)

if __name__ == "__main__":
    # root_dir='taobao'
    # output_dir='taobao_excel'
    # root_dir='JD'
    # output_dir='JD_excel'
    root_dir='pinduoduo_v1'
    output_dir='pinduoduo_v1_excel'
    list_files=os.listdir(root_dir)
    list_files=[item for item in list_files if(item.split('.')[-1]=='csv')]
    create_root(output_dir)
    for file in list_files:
        src_path=os.path.join(root_dir,file)
        excel_name=file[:-3]+'xls'
        print(excel_name)
        dest_path=os.path.join(output_dir,excel_name)
        convert(src_path,dest_path)
