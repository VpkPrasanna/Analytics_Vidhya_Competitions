# -*- coding: utf-8 -*-
"""Analytics

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xW0K0ZCsm7zcelY0fmH6mNQ9pm_O7a8_
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score,confusion_matrix,precision_score,f1_score
import lightgbm as lgb

train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')
train.head()

train.describe()

train.info()

"""**Analysis and Visuvalization**"""

corr = train.corr()
plt.figure(figsize=(10,10))
ax = sns.heatmap(corr,vmin=-1, vmax=1, center=0,cmap='coolwarm',square=True)

# Age,lenght of service , KPI,awards won

plt.hist(train['age'])

plt.hist(train['awards_won?'])

sns.barplot(x = 'awards_won?',y = 'KPIs_met >80%',data=train)

"""# Missing values
**Finding missing values**
"""

print(set(train['previous_year_rating'].isna()))
print(set(train['age'].isna()))
print(set(train['education'].isna()))
print(set(train['gender'].isna()))
print(set(train['recruitment_channel'].isna()))
print(set(train['no_of_trainings'].isna()))
print(set(train['length_of_service'].isna()))
print(set(train['KPIs_met >80%'].isna()))
print(set(train['awards_won?'].isna()))
print(set(train['avg_training_score'].isna()))
print(set(train['is_promoted'].isna()))

"""**This concludes the above column have missing values in them**

#Categorical feature can be imputed by mode or Bfill or Ffill
#Numerical feature can be treated by mean mode bfill or Ffill
"""

print(train.isnull().sum())
print("***"*20)
print(test.isnull().sum())

train['education'].replace(np.nan,"Bachelor's",inplace=True)
test['education'].replace(np.nan,"Bachelor's",inplace=True)

train['education'].replace("Master's & above",3,inplace=True)
test['education'].replace("Master's & above",3,inplace=True)
train['education'].replace("Bachelor's",2,inplace=True)
test['education'].replace("Bachelor's",2,inplace=True)
train['education'].replace("Below Secondary",1,inplace=True)
test['education'].replace("Below Secondary",1,inplace=True)

train['previous_year_rating'].replace(np.nan,3.,inplace=True)
test['previous_year_rating'].replace(np.nan,3.,inplace=True)

train['sum_metric'] = train['awards_won?']+train['KPIs_met >80%'] + train['previous_year_rating']
test['sum_metric'] = test['awards_won?']+test['KPIs_met >80%'] + test['previous_year_rating']

train['tot_score'] = train['avg_training_score'] * train['no_of_trainings']
test['tot_score'] = test['avg_training_score'] * test['no_of_trainings']

train[train['is_promoted']==1].groupby('previous_year_rating')['is_promoted'].count()
train.groupby('previous_year_rating')['is_promoted'].count()

train.isna().sum()
test.isna().sum()

train.head()

#Treating Gender Column
# train['gender'].fillna(train['gender'].mode()[0], inplace = True)
# test['gender'].fillna(test['gender'].mode()[0],inplace = True)

#Treating recruitment_channel Column
# train['recruitment_channel'].fillna(train['recruitment_channel'].mode()[0], inplace = True)
# test['recruitment_channel'].fillna(test['recruitment_channel'].mode()[0],inplace = True)

#Treating no_of_trainings Column
# train['no_of_trainings'].fillna(train['no_of_trainings'].mode()[0],inplace = True)
# test['no_of_trainings'].fillna(test['no_of_trainings'].mode()[0],inplace = True)

#Treating age Column
# train['age'].fillna(np.ceil(train['age'].mean()),inplace = True)
# test['age'].fillna(np.ceil(train['age'].mean()),inplace = True)

#Treating length_of_service Column
# train['length_of_service'].fillna(np.ceil(train['length_of_service'].mean()),inplace = True)
# test['length_of_service'].fillna(np.ceil(test['length_of_service'].mean()),inplace = True)

#Treating KPIs_met Column
# train['KPIs_met >80%'].fillna(train['KPIs_met >80%'].mode()[0],inplace = True)
# test['KPIs_met >80%'].fillna(test['KPIs_met >80%'].mode()[0],inplace = True)

#Treating awards_won Column
# train['awards_won?'].fillna(train['awards_won?'].mode()[0],inplace = True)
# test['awards_won?'].fillna(test['awards_won?'].mode()[0],inplace = True)

#Treating avg_training_score Column
# train['avg_training_score'].fillna(train['avg_training_score'].mode()[0],inplace = True)
# test['avg_training_score'].fillna(test['avg_training_score'].mode()[0],inplace = True)

#Treating education Column
# train['education'].fillna(train['education'].mode()[0],inplace = True)
# test['education'].fillna(test['education'].mode()[0],inplace = True)

#Treating previous_year_rating Column
# train['previous_year_rating'].fillna(np.ceil(train['previous_year_rating'].mean()),inplace = True)
# test['previous_year_rating'].fillna(np.ceil(test['previous_year_rating'].mean()),inplace = True)

#Treating is_promoted Column
# train['is_promoted'].fillna(np.ceil(train['is_promoted'].mean()),inplace = True)

print(train.isnull().sum())
print("***"*20)
print(test.isnull().sum())

train['previous_year_rating'].value_counts().sort_index().head(50).plot.bar()

fig,axrr=plt.subplots(2,2,figsize=(14,8))

df= train[train.department.isin(train.department.value_counts().head(10).index)]
sns.boxplot(x='department',y='avg_training_score',data=df,ax=axrr[0][0])


test['avg_training_score'].value_counts().sort_index()[:1000].plot.area(ax=axrr[0][1])


sns.boxplot(x='is_promoted',y='avg_training_score',data=train,ax=axrr[1][0])

sns.countplot(train['KPIs_met >80%'],ax=axrr[1][1])

train.plot.hist(alpha=0.5, bins=10, grid=True, legend=None)

"""#Encoding the categorical data

**Before Encoding drop the un necesary column**
"""

train = train.drop(['employee_id'],axis = 1)
test = test.drop(['employee_id'],axis = 1)

le = LabelEncoder()
train['department'] = le.fit_transform(train['department'])
test['department'] = le.transform(test['department'])
train['region'] = le.fit_transform(train['region'])
test['region'] = le.transform(test['region'])
train['education'] = le.fit_transform(train['education'])
test['education'] = le.transform(test['education'])
train['gender'] = le.fit_transform(train['gender'])
test['gender'] = le.transform(test['gender'])
train['recruitment_channel'] = le.fit_transform(train['recruitment_channel'])
test['recruitment_channel'] = le.transform(test['recruitment_channel'])

train.head()

train1 = train.drop(['recruitment_channel'],axis = 1)
test1 = test.drop(['recruitment_channel'],axis = 1)

train1.columns

test1.columns



"""#seperating X and Y from Train data"""

y = train['is_promoted']
x = train.drop(['is_promoted'],axis = 1)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

"""#Creating Model

**XG Boost Classifier**
"""

best = lgb.LGBMClassifier()
best.fit(X_train,y_train,eval_metric='logloss')

lgbm_predicted = best.predict(X_test)

len(lgbm_predicted)

lgbm_acc = accuracy_score(y_test,lgbm_predicted)
print(lgbm_acc)

plt.figure(figsize=(8,8))
df_cm = pd.DataFrame(confusion_matrix(y_test, lgbm_predicted), range(2),range(2))
sns.set(font_scale=1.4)#for label size
sns.heatmap(df_cm, annot=True,annot_kws={"size": 16}, fmt='g')
plt.xlabel('Predicted Class')
plt.ylabel('Original Class')

lgbm_precision = precision_score(y_test,lgbm_predicted)
print(lgbm_precision)

lgbm_f1 = f1_score(y_test,lgbm_predicted)
print(lgbm_f1)

lgbm_submi = pd.read_csv('sample_submission.csv')
print(lgbm_submi.head())

lgbm_submi['is_promoted'] = best.predict(test)
print(lgbm_submi.head())
lgbm_submi.to_csv('lgbm_final.csv',index=False)

"""#Logistic Regression"""

clf = LogisticRegression(random_state=0,solver = 'liblinear')
clf.fit(X_train,y_train)

y_pred=clf.predict(X_test)

len(y_pred)

# matrix = confusion_matrix(y_test,y_pred)
value = accuracy_score(y_test,y_pred)
print(value)

plt.figure(figsize=(8,8))
df_cm = pd.DataFrame(confusion_matrix(y_test, y_pred), range(2),range(2))
sns.set(font_scale=1.4)#for label size
sns.heatmap(df_cm, annot=True,annot_kws={"size": 16}, fmt='g')
plt.xlabel('Predicted Class')
plt.ylabel('Original Class')

pres = precision_score(y_test, y_pred)
print(pres)

f1 = f1_score(y_test, y_pred,average='micro')
print(f1)
print(f1*100)

metrics.plot_roc_curve(clf,X_test,y_test)

from sklearn.metrics import recall_score
from sklearn.preprocessing import StandardScaler
recal = recall_score(y_test,y_pred)
print(recal)

submi = pd.read_csv('sample_submission.csv')
print(submi.head())

predddd = clf.predict(test)
print(predddd)

submi['is_promoted'] = clf.predict(test)

submi.to_csv("Final_submission.csv", index=False)

"""#Other Algorithm"""

date = CalibratedClassifierCV(clf,method='sigmoid',cv = 5)

date.fit(X_train,y_train)

predd = date.predict(X_test)

accuracy = accuracy_score(y_test,predd)
print(accuracy)

f1_scores = f1_score(y_test,predd)
print(f1_scores)

train.skew()

train.hist(bins=3)

scaller = StandardScaler()
new_data = scaller.fit(train)

print(scaller.mean_)

import numpy as np
data = np.random.randn(50000)  * 20 + 20

