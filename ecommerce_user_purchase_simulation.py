# -*- coding: utf-8 -*-
"""
NOTES:

The following script generates simulated ecommerce data for
'Super Bad Product' company's website. The data is intended to be used for
training purposes for various data science alogithms.

The script makes use of various functions from the built in 'random' library
for the generation of the data.

@author: datacourses
"""

import pandas as pd
import random
import numpy as np

#### Generate a list of visitors with an exponentially decreasing distribution

visits = [round(random.expovariate(.125),0) for i in np.arange(0,1000000)]
s = pd.Series(visits)
visits = s + 1

v = pd.DataFrame({'visits':visits,'purchases':s.sample(n=visits.count()/12)})
v.purchases = v.purchases/4
v.purchases = v.purchases.round()

prices = [0.99, 2.99, 14.99, 14.99, 2.50, 399, 1.99, 7.99, 7.50, 4.11, 150, 82.45, 0.17]

f = v[v.purchases.notnull()]

ps = []
for i in f.purchases:
    a = 0
    p = []
    for l in np.arange(0,i):
        if a <= i:
            p.append(random.choice(prices))
        a = a+1
    ps.append(p)

f['purchase_details'] = ps

a = []
for l in f['purchase_details']:
    y = sum(l)
    a.append(y)

f['total_spend'] = a

### Generate 'Returned' Items (only 1 item)
#select returns from purchase details with likelihood of 1/20th

return_odds = .05

a = []
for l in f['purchase_details']:
    if random.random() <= return_odds:
        try:
            i = random.choice(l)
        except IndexError:
            i = 0
    else:
        i = 0
    a.append(i)

f['returns'] = a

#### Generate a column showing whether a user has taken advantage of discounted pricing

discount_prices = [4.11,.17]

a = []
for l in f['purchase_details']:
    c = 0
    for p in discount_prices:
        y = l.count(p)
        c = c + y
    a.append(c)

f['discountedprices'] = a

#### Merge puchase related data back into main dataframe

df = v.join(f[['purchase_details','total_spend','returns','discountedprices']],how='left')

#### Generate abandoned items in the cart of the users

abandon_odds = .125

ai = []
for l in df['visits']:
    if random.random() <= abandon_odds:
        ai.append(round(random.expovariate(.125),0))
    else:
        ai.append(0)
        
df['abandoneditems'] = ai

#### GENERATE USER SPECIFIC DATA

has_account = .241

a = []
for l in df['visits']:
    if random.random() <= has_account:
        i = 1
    else:
        i = 0
    a.append(i)
    
df['has_account'] = a

#### GENERATE USER EMAILS

email_ends = ['facebook.com','gmail.com','yahoo.com','hotmail.com','snet.com','att.com','provider.com','gov.com','mil.com']

alpha = 'abcdefghijklmnopqrstuvwxzy'

account_list = df[df['has_account'] == 1]

email_address = []
for i in account_list['visits']:
    prefix_len = random.randrange(5,34)
    letters = ''
    for i in np.arange(prefix_len):
        letters = letters+alpha[random.randrange(0,25)]
    address = letters+'@'+random.choice(email_ends)
    email_address.append(address)

account_list['emailaddress'] = email_address

df = df.join(account_list[['emailaddress']],how='left')

#### Write it all to a dataframe & .pkl file for posterity
df.to_csv('superbadproduct_purchase_history-test.csv', index=False)
df.to_pickle('superbadproduct_purchase_history-test.pkl')