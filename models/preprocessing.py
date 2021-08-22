#!/usr/bin/env python
# coding: utf-8

# In[66]:


import pandas as pd
import pyarrow.parquet as pq
import datetime


# In[67]:


df = pq.read_table(source="/home/toliman/Desktop/257-2021-4-player-log.parquet").to_pandas()


# In[68]:


print(df.shape)
new_df = pd.DataFrame(columns=('month', 'week_day', 'half_hour', 'efficiency', 'unix', 'views'), )


# In[69]:


for i in range(df.shape[0]):
    if (i % 1000 == 0):
        print(i // 1000)
    obj = df.loc[i]
    in_t = datetime.datetime.fromtimestamp(obj['DateTimeInTick'] / 1000)
    out_t = datetime.datetime.fromtimestamp(obj['DateTimeOutTick'] / 1000)
    month_1 = in_t.month
    month_2 = out_t.month
    weekday_1 = in_t.weekday()
    weekday_2 = out_t.weekday()
    halfhour_1 = 2 * in_t.hour + 1 + int(in_t.minute >= 30)
    halfhour_2 = 2 * in_t.hour + 1 + int(in_t.minute >= 30)
    efficiency = obj['MacCountAll'] / obj['Duration']

    new_df = new_df.append({'month': month_1, 'week_day': weekday_1, 'half_hour': halfhour_1, 'efficiency': efficiency,
                            'unix': obj['DateTimeOutTick'], 'views': int(obj['MacCountAll'])},
                           ignore_index=True)

    if month_1 != month_2 or weekday_1 != weekday_2 or halfhour_1 != halfhour_2:
        new_df = new_df.append(
            {'month': month_2, 'week_day': weekday_2, 'half_hour': halfhour_2, 'efficiency': efficiency,
             'unix': obj['DateTimeOutTick'], 'views': int(obj['MacCountAll'])},
            ignore_index=True)


# In[70]:


new_df.shape


# In[71]:


new_df


# In[72]:


new_df.to_csv('/home/toliman/Desktop/preprocessing_data.csv')

