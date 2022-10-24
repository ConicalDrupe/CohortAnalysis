# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 12:51:17 2022

@author: Christopher
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_excel("OnlineRetail.xlsx")
data.info()

#drop rows with no customer ID
data = data.dropna(subset='CustomerID')