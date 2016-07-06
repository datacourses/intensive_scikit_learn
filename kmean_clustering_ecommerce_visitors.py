# -*- coding: utf-8 -*-
"""
NOTES:

NOTES:

The following script generates performs a basic kmeans clustering on 
'Super Bad Product' company's website visitor data.

@author: datacourses
"""

import pandas as pd
from sklearn.cluster import KMeans
import seaborn
import numpy as np

### First, let's import our dataframe
df = pd.read_csv('superbadproduct_purchase_history-test.csv')

### let's get rid of some of the superluous columns in this exercise
# we really only care about the interger and float values here as that's what
# kmeans requires to perform it's distance calculations

df = df[['purchases','visits','total_spend','returns','emailaddress']]

#we can see there are many NaN values - these will be replaced with 0
df[['purchases','visits','total_spend','returns']] = df[['purchases','visits','total_spend','returns']].fillna(0)

#### START K-Means for k between 2 and 15

k_range = np.arange(2,15)

#set the dataframe only to the numeric variables
m = df[['purchases','visits','total_spend','returns']]

# Compute the RSS for each k for 2 to 15 clusters

inertia_dict = dict()
centers_dict = dict()
for k in k_range:
    km = KMeans(n_clusters=k)
    km.fit(m)
    #writes the labels for each k back to the dataframe
    df['labels_k_{}'.format(str(k))] = km.labels_
    centers_dict[k] = km.cluster_centers_
    inertia_dict[k] = km.inertia_
    print str(k) + ' clustering completed...'

print 'all done...'
    
df.to_csv('k_means_dataframe_ecommerce_users.csv')