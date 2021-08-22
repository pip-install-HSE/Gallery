#!/usr/bin/env python
# coding: utf-8

# In[260]:


from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow.keras.losses import MSE, MAE
from tensorflow.keras.activations import elu
from tensorflow.keras.optimizers import Adam, RMSprop
import numpy as np
import pandas as pd
import datetime


# In[261]:


train_x = np.load('/home/toliman/Desktop/train_x.npy')
train_y = np.load('/home/toliman/Desktop/train_y.npy')
targets = np.load('/home/toliman/Desktop/targets.npy')


# In[265]:


train_x


# In[ ]:


from sklearn.model_selection import train_test_split

x_train, x_val, y_train, y_val = train_test_split(train_x, train_y, shuffle=False)


# In[ ]:


network = Sequential(
    [
        layers.Dense(64, input_shape=(train_x.shape[1],), activation='relu'),
        layers.Dense(96, activation='relu'),
        layers.Dense(128, activation='relu'),
        layers.Dense(128, activation='relu'),
        layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(16, activation='relu'),
        layers.Dense(1, activation='sigmoid'),
    ]
)

network.summary()


# In[211]:


from tensorflow.keras.metrics import RootMeanSquaredError

network.compile(
    optimizer=RMSprop(learning_rate=.00025),
    loss=MAE,
    metrics=[RootMeanSquaredError(), ],
)


# In[212]:


network.fit(
    x_train,
    y_train,
    batch_size=128,
    epochs=30,
    validation_data=(x_val, y_val,),
)

network.save('billyboard.v4.h5')


# In[229]:


x = np.random.choice(train_x.shape[0], 100, replace=False)


# In[ ]:


pred = network.predict(train_x[x])

ar = train_y[x]

print(list(zip(pred, ar)))


# In[214]:




