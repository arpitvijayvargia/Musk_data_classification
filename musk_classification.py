# -*- coding: utf-8 -*-
"""Musk_classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FiHA480wTSu8JehbqW880zTFR_oQJgwS
"""

#importing libraries      
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#importing dataset from the drive
data = pd.read_csv('/content/drive/My Drive/musk_csv.csv')
data.head()

#some info about the dataset
data.info

data.nunique()

#drop unwanted columns
data.drop(['molecule_name','ID','conformation_name'],axis=1,inplace=True)

#let's see our new transformed data
data.head()

#let's check for null values
data.isnull().values.any()

#split out data into 80% traning and 20% testing
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(data,data['class'], test_size = 0.20,random_state=120)

print(X_train.shape)
print(X_test.shape)

#let's import some DL library's
from sklearn.metrics import confusion_matrix, precision_score
from keras.layers import Dense,Dropout
from keras.models import Sequential
from keras.regularizers import l2
import matplotlib.pyplot as plt

#Define the Model - 3 layers (2 hidden layers with 100 nodes each and 1 output layer with a single)

#defifne a sequentail Model
model = Sequential()

#Hidden Layer-1
model.add(Dense(400,activation='sigmoid',input_dim=167,kernel_regularizer=l2(0.02)))
model.add(Dropout(0.3, noise_shape=None, seed=None))

#Hidden Layer-2
model.add(Dense(400,activation = 'relu',kernel_regularizer=l2(0.01)))
model.add(Dropout(0.3, noise_shape=None, seed=None))

#Hidden Layer-3
model.add(Dense(400,activation = 'relu',kernel_regularizer=l2(0.01)))
model.add(Dropout(0.3, noise_shape=None, seed=None))

#Output layer
model.add(Dense(1,activation='sigmoid'))

from keras import optimizers

l_rate=0.00001
training_epoch=70
batch_size=500
adma=optimizers.adam(lr=l_rate)

#compiling the model
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

op=model.fit(X_train,Y_train,batch_size=batch_size,epochs=training_epoch,verbose=2,validation_data=(X_test,Y_test))

print(op.history.keys())

#Let's plot how our loss behaves at each epochs
plt.plot(op.history['loss'],label='train')
plt.xlabel('epochs')
plt.plot(op.history['val_loss'],label='test')
plt.ylabel('loss')
plt.legend()
plt.show()

#let's see the accuracy per epochs
plt.plot(op.history['acc'],label='train')
plt.xlabel('epochs')
plt.plot(op.history['val_acc'],label='test')
plt.ylabel('accuracy')
plt.legend()
plt.show()

y_pred = model.predict(X_test)
rounded = [round(x[0]) for x in y_pred]
y_pred1 = np.array(rounded,dtype='int64')

confusion_matrix(Y_test,y_pred1)

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score

# accuracy: (tp + tn) / (p + n)
accuracy = accuracy_score(Y_test,y_pred1)
print('Accuracy: %f' % accuracy)
# precision tp / (tp + fp)
precision = precision_score(Y_test,y_pred1)
print('Precision: %f' % precision)

Y_pred=model.predict(X_test).astype('int').flatten()
print(Y_pred)

from sklearn.metrics import classification_report
cls = classification_report(Y_test,Y_pred)
print(cls)

#save the model
model.save("Calssifier.h5")

