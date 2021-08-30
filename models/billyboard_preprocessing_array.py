#!/usr/bin/env python
# coding: utf-8

# In[200]:


from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow.keras.losses import MSE, MAE
from tensorflow.keras.activations import elu
from tensorflow.keras.optimizers import Adam, RMSprop
import numpy as np
import pandas as pd
import datetime
import tqdm


# In[201]:


def unix_to_month(int_unix):
    return datetime.datetime.fromtimestamp(int_unix).month - 1


def unix_to_day(int_unix):
    return datetime.datetime.fromtimestamp(int_unix).day - 1


def unix_to_half_hour_index(int_unix):
    obj = datetime.datetime.fromtimestamp(int_unix)
    return 1 + obj.hour * 2 + obj.minute // 30 - 1


def fill_targets(data: pd.DataFrame):
    targets = np.zeros(shape=(12, 31, 49))
    for i in tqdm.tqdm(range(max(data.shape[0], 100))):
        obj = data.loc[i]
        day = unix_to_day(int(obj['unix']) // 1000)
        half_hour = unix_to_half_hour_index(int(obj['unix']) // 1000)
        month = unix_to_month(int(obj['unix']) // 1000)
        targets[month][day][half_hour] += int(obj['views'])
    return targets


# In[7]:




import pandas as pd

data = pd.read_csv('/home/toliman/Desktop/holidays_new_mean_sum_dist_month.csv')


# In[8]:


data


# In[ ]:


# print(data.columns)
# print(data.values)
# data = data.drop(columns=['unix', ], axis=1)

targets = fill_targets(data)


# In[203]:



# for x in targets:
#     print(x.max())


# In[204]:


train_y = np.zeros(shape=(data.shape[0]))


# In[205]:


for i in tqdm.tqdm(range(max(data.shape[0], 100))):
    obj = data.loc[i]
    day = unix_to_day(int(obj['unix']) // 1000)
    half_hour = unix_to_half_hour_index(int(obj['unix']) // 1000)
    month = unix_to_month(int(obj['unix']) // 1000)
    train_y[i] = targets[month][day][half_hour]


# In[206]:


train_y -= train_y.min()
train_y /= train_y.max()

np.save('/home/toliman/Desktop/targets', targets)
np.save('/home/toliman/Desktop/train_y', train_y)

data = data.drop('unix', axis=1)


# In[208]:


train_x = data.values

for i in tqdm.tqdm(range(max(train_x.shape[0], 100))):
    train_x[i] -= train_x[i].min()
    train_x[i] /= train_x[i].max()

np.save('/home/toliman/Desktop/train_x', train_x)

exit(0)


# In[ ]:


stats = np.zeros(shape=(49,))
for x in targets:
    stats += x

stats /= targets.shape[0]

from matplotlib import pyplot as plt

plt.plot(list(range(0, 49)), stats, color='red')
plt.show()

