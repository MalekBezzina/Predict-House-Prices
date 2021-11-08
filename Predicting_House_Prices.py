#### TASK 1 importing  Libraries ####

import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf

from utils import *
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import  Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, LambdaCallback

from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
print('libraries imported')
#### TASK 2 importing  the DATA ####

df=pd.read_csv('data.csv',names=column_names)
print(df.head())

#check missing data
print(df.isna().sum())

#### TASK 3 DATA Normalization ####

df=df.iloc[:,1:]
df_norm=(df-df.mean())/df.std()
print(df_norm.head())

#convert label value
y_mean=df['price'].mean()
y_std=df['price'].std()

def convert_label_value(pred):
    return int(pred *y_std + y_mean )

print(convert_label_value(0.350088))

#### TASK 4 DATA Noralization ####

#select features
x=df_norm.iloc[:,:6]
print(x.head())

#select labels
y=df_norm.iloc[:,-1]
print(y.head())

#feature and label values
x_arr=x.values
y_arr=y.values
print('features array shape',x_arr.shape)
print('label array shape',y_arr.shape)


#train and test split
x_train,x_test,y_train,y_test=train_test_split(x_arr,y_arr,test_size=0.05,random_state=0)
print('training set',x_train.shape, y_train.shape)
print('test set',x_test.shape,y_test.shape)

#### TASK 5  create the MODEL ####

def get_model():
    model=Sequential([
        Dense(10,input_shape=(6,),activation='relu'),
        Dense(20,activation='relu'),
        Dense(5,activation='relu'),
        Dense(1)    
    ])

    model.compile(
        loss='mse',
        optimizer='adam'
    )
    return model

get_model().summary()

#### TASK 6 MODEL training ####
es_cb=EarlyStopping(monitor='val_loss',patience=5)

model=get_model()
preds_on_untrained=model.predict(x_test)

history=model.fit(
    x_train,y_train,
    validation_data=(x_test,y_test),
    epochs=100,
    callbacks=[es_cb]
    )

#plot training and validation 

plot_loss(history)

#### TASK 7 predictions ####

#plot raw prediction
preds_on_trained=model.predict(x_test)
compare_predictions(preds_on_untrained,preds_on_trained,y_test)

#plot price predictions
price_untrained=[convert_label_value(y) for y in preds_on_untrained]
price_trained=[convert_label_value(y) for y in preds_on_trained]
price_test=[convert_label_value(y) for y in y_test]

compare_predictions(price_untrained,price_trained,price_test)











































