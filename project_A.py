import pandas as pd
from bs4 import BeautifulSoup
import requests

# 取得soup
def get_soup(url):
    html= requests.get(url)
    content = html.text
    soup = BeautifulSoup(content,'html.parser')
    return soup

# 分析网页
def analyze(soup):
    #找到总表
    temp = soup.find('div',class_="search-result-list")
    # 找到总清单
    items = temp.find_all('a')
    # 建立空列表
    df2=pd.DataFrame(columns = ['name','名称','价格','产品图片链接'])
    temp2= {}
    for a in items:
        #根据不同属性，取得需要的字符串信息
        #取得链接
        temp2['name']= str(a.get('href'))
        # 取得文本
        temp2['名称']= a.find('p',class_= "cx-name text-hover").get_text()
        temp2['价格']= a.find('p',class_= "cx-price").get_text()
        # 取得链接
        temp2['产品图片链接']=a.find('img').get('src')
        temp2['产品图片链接']='http:'+temp2['产品图片链接']
        df2= df2.append(temp2, ignore_index=True)
    return df2

# 针对scrap 的dataframe数据进行整理

def sort_out(re):
    # name 切片
    re['name']=re['name'].apply(lambda re: re[1:-1])
    # 取得最高和最低价格切片
    re['最高价格']= re['价格'].map(lambda re:re[-6:])
    re['最低价格']=re['价格'].apply(lambda re:re[0:-7])
    # 最低价格如果不是空值，加上“万”
    re['最低价格']=re['最低价格'].map(lambda re:re+"万" if len(re)>0 else re)
    # 最低价格是空值，根据mask条件，增加辅助列
    re['最低价格长度']= re['最低价格'].map(lambda re:len(re))
    re['最低价格']=re['最低价格'].mask(re['最低价格长度']==0,re['最高价格'])
    # 去除多余的列
    re = re.drop(['name','价格','最低价格长度'],axis= 1,inplace=True)
    #列位置调整,但是实际没有出来效果？？？？为什么？？？
    columns= ['名称','最低价格','最高价格','产品图片链接']
    re= pd.DataFrame(re,columns= columns)
    return re

if __name__ =='__main__':

    # 循环取得网页数据，生成总表
    base_url = 'http://car.bitauto.com/xuanchegongju/?mid=8&page='
    page_num = 3
    result= pd.DataFrame(columns= ['name','名称','价格','产品图片链接'])

    for i in range(page_num):
        request_url= base_url+str(i+1)
        soup = get_soup(request_url)
        df = analyze(soup)
        result = result.append(df,ignore_index = True)
        
    sort_out(result)
    print(result)
    #下面两句为调整列的位置，sort_out中，没能完成排序，这里再做一遍
    columns= ['名称','最低价格','最高价格','产品图片链接']
    result= pd.DataFrame(result,columns= columns)
    result.to_csv('project_A_cardata.csv',index= False)