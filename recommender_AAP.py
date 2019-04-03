import graphlab as gl
import graphlab.aggregate as agg
import pandas as pd
import numpy as np
#import scipy
#import matplotlib.pyplot as plt
#import seaborn as sns
import math as math
import pyodbc
#import pysftp

# Create the connection to the sql server w.r.t to the DNS set
conn = pyodbc.connect("DSN=sq02", autocommit=True)

# SQL query across the tables
sql = """

-- dataB2B for AAP with aditional condition of I.codMarchio = 'N04' AND fsc.[Shortcut Dimension 1 Code]='AA-NK
SELECT DISTINCT F.CustomerKey AS customerKey, C.Name AS customerName, I.[Vendor Item No_] AS vendorItemNo,
	I.[Vendor No_] AS vendorNo, I.ItemKey as itemKey, I.Description AS itemDescription, I.marchio, I.codMarchio, I.sport, I.reparto, I.sesso, I.tipo
FROM [3A_DWH].[dbo].[FactSalesOrder] AS F
  JOIN [3A_DWH].[dbo].[DimItem] AS I
  ON I.ItemKey = F.ItemKey
  JOIN [3A_DWH].[dbo].[DimCustomer] AS C
  ON C.CustomerKey = F.CustomerKey
  join [3A_DWH].[dbo].[FactSalesConditions] as fsc
  on C.CustomerKey = fsc.CustomerKey and
  i.codMarchio = fsc.[Brand Code]
  WHERE C.Name NOT LIKE 'T%' AND YEAR(F.[Order Date]) > 2016 AND I.Company = '3A dei F_lli Antonini S_p_a_' and
  F.[BusinessType Code]='B2B' AND I.codMarchio = 'N04' AND fsc.[Shortcut Dimension 1 Code]='AA-NK'
  -- example
  --and C.CustomerKey like '%c06423%'
  ORDER BY F.CustomerKey, I.[ItemKey];
  
"""

# Read sql query output to panda dataframe
df = pd.io.sql.read_sql(sql, conn)

# Convert Dataframe to SFrame
dataB2B = gl.SFrame(df)

# Save the sframe data and print the result for visualization
dataB2B.save('./dataset/dataB2B_AAP.csv', format='csv')
print dataB2B.num_rows(), '\n', dataB2B.column_names(), '\n', dataB2B.head(), '\n', df.head()

########## Derive dictionaries from item/product
dicCustomer = dataB2B.select_columns(['customerKey', 'customerName']).unique()
dicItem = dataB2B.select_columns(['itemKey', 'vendorItemNo', 'vendorNo', 'itemDescription', 'marchio', 'codMarchio', 'sport', 'reparto', 'sesso', 'tipo']).unique()

#### Count unique users/Products
users = dataB2B['customerKey'].unique()
products = dataB2B['itemKey'].unique()

########## Split dataset into train and test
train_data, test_data = dataB2B.random_split(0.8, seed=0)

### POPULARITY ####

########## Popularity-based recommender
model_pop = gl.popularity_recommender.create(dataB2B, user_id='customerKey', item_id='itemKey')
########## Recommned product for users using Popularity-based recommender
recommended_pop = model_pop.recommend(users)
recommended_pop = recommended_pop.join(dicCustomer, on = 'customerKey', how = 'inner').join(dicItem, on = 'itemKey', how = 'inner')
# recommended_pop = model_pop.recommend([dataB2B[dataB2B['customerName']=='GONZATO SRL']['customerKey'][0]]).join(dicCustomer, on = 'customerKey', how = 'inner').join(dicItem, on = 'itemKey', how = 'inner')

### PERSONALIZED ####

########## Personalized Recommender
model_pers = gl.item_similarity_recommender.create(dataB2B, user_id='customerKey', item_id='itemKey')
########## Recommned product for users using Personalized recommender
recommended_pers = model_pop.recommend(users)
recommended_pers = recommended_pers.join(dicCustomer, on = 'customerKey', how = 'inner').join(dicItem, on = 'itemKey', how = 'inner')

########## Full List of Most Similar Items within N04

similar_purchases = model_pers.get_similar_items(products)
similar_purchases = similar_purchases.join(dicItem, on = 'itemKey', how = 'inner').join(dicItem, on = {'similar':'itemKey'}, how = 'inner')
similar_purchases.head(10)

########## EXPORT THE OUTPUTS ############

########## Export PERS_output as json/csv
recommended_pers.export_json('./output/personalizedRecommend_AAP.json', orient='records')
recommended_pers.save('./output/personalizedRecommend_AAP.csv', format='csv')

########## Export POP_output as json/csv
#recommended_pop.export_json('./output/AAP/popularRecommend_AAP.json', orient='records')
#recommended_pop.save('./output/AAP/popularRecommend_AAP.csv', format='csv')

########## Export of most Similarly purchased product pairs as json/csv
#similar_purchases.export_json('./output/similarPurchases_AAP.json', orient='records')
#similar_purchases.save('./output/similarPurchases_AAP.csv', format='csv')
