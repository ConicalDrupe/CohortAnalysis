# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 12:51:17 2022

@author: Christopher
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_excel("OnlineRetail.xlsx")
#data.info()

#drop rows with no customer ID
data = data.dropna(subset=['CustomerID'])
data.info()

#%%
#create an invoice month
import datetime as dt
#function for month: returns(year,month,day=1)
def get_month(x):
    return dt.datetime(x.year,x.month,1)

#apply function
data['InvoiceMonth'] = data['InvoiceDate'].apply(get_month)
data.tail()

#%%
#[Time Cohort] create a column index w/ date: AKA first time our customer was aquired
data['Cohort Month'] = data.groupby('CustomerID')['InvoiceMonth'].transform('min')
data.head(30)

#%%
#Create a date element function to get a series for subtraction
def get_date_elements(df,col):
    day = df[col].dt.day
    month = df[col].dt.month
    year = df[col].dt.year
    return day, month, year

#Get date elements of Invoice Month
_,Invoice_month,Invoice_year = get_date_elements(data,'InvoiceMonth')
#Get date elements of Cohort Month
_,Cohort_month,Cohort_year = get_date_elements(data,'Cohort Month')

#%%
#Create a Cohort Index (when user was aquired)
year_diff = Invoice_year - Cohort_year
month_diff = Invoice_month - Cohort_month
#Cohort index calculates how many months its been since aquisition
data['CohortIndex'] = year_diff*12 + month_diff + 1

#%%
#Count unique customer ID by grouping by cohort month and cohort index
cohort_data = data.groupby(['Cohort Month','CohortIndex'])['CustomerID'].apply(pd.Series.nunique).reset_index()

#%%
#Create a Pivot Table
cohort_table = cohort_data.pivot(index='Cohort Month', columns = ['CohortIndex'],values='CustomerID')

#%%
#change index
cohort_table.index = cohort_table.index.strftime('%B %Y') 

#Visualize our results
plt.figure(figsize=(21,10))
sns.heatmap(cohort_table,annot=True,cmap='Blues')

#%%
#Create percentages
new_cohort_table = cohort_table.divide(cohort_table.iloc[:,0],axis=0)


plt.figure(figsize=(21,10))
fig = sns.heatmap(new_cohort_table,annot=True,cmap='magma',fmt='.0%')
#fig.figure.savefig("CohortHeatMap.png")
