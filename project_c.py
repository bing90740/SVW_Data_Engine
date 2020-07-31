from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd
import numpy as np
from pandas.api.types import is_string_dtype

# 数据加载，train_x列名更改
data= pd.read_csv('./ProjectC/CarPrice_Assignment.csv')
train_x = data.drop(['car_ID','CarName'], axis = 1)
train_x.columns = list(range(24))

# 将非数值的列 LabelEncoder

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
for i in range(23):
    if is_string_dtype(train_x[i]):
        train_x[i] = le.fit_transform(train_x[i])

# 规范化到[0,1]空间
min_max_sacler = preprocessing.MinMaxScaler()
train_x = min_max_sacler.fit_transform(train_x)
pd.DataFrame(train_x).to_csv('project_c_temp.csv',index = False)


# K-Means 手肘法：统计不同K取值的误差平方和
import matplotlib.pyplot as plt
sse = []
for k in range(1, 50):
	# kmeans算法
	kmeans = KMeans(n_clusters=k)
	kmeans.fit(train_x)
	# 计算inertia簇内误差平方和
	sse.append(kmeans.inertia_)
x = range(1, 50)
plt.xlabel('K')
plt.ylabel('SSE')
plt.plot(x, sse, 'o-')
plt.show()

# 使用KMeans聚类,   根据手肘图，K设为20
kmeans= KMeans(n_clusters= 20)
kmeans.fit(train_x)
predict_y= kmeans.predict(train_x)
# 合并聚类结果，插入到原数据中
result = pd.concat((data,pd.DataFrame(predict_y)),axis = 1)
result.rename({0:u'聚类结果'},axis = 1,inplace= True)
#print(result)
result.to_csv("project_c_kmeans.csv",index=False)