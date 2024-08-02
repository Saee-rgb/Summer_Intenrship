# -*- coding: utf-8 -*-
"""mytsdataset_latest.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ipHVYRHJhkbKm5dlv9jz-b5HUBDl9fjr
"""

# -*- coding: utf-8 -*-
"""MyTSDataSet.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1frV9F4nwj45uPhjHqJrwylev33GpWL5n
"""

import torch
from torch.utils.data import TensorDataset, DataLoader
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

class MyTimeSeriesDataset(object):
    def __init__(self, df,lags, horizon_length , standardise , differencing , exo ):
        #  ''' exo is list of column names

        self.df = df
        self.lags = lags
        self.horizon_length = horizon_length
        self.standardise = standardise
        self.differencing = differencing
        self.scalers = {}
        self.exo = exo

    def preprocess_mydata(self):
        df = self.df
        lags = self.lags
        horizon_length = self.horizon_length
        standardise = self.standardise
        differencing = self.differencing
        exo = self.exo

        train , test = train_test_split(df , test_size = horizon_length , shuffle = False)



        if standardise:
           # Standardizing the data
          for col in df.columns:
            scaler = StandardScaler()
            train.loc[:, col] = scaler.fit_transform(train[[col]])
            test.loc[:, col] = scaler.transform(test[[col]])
            self.scalers[col] = scaler

        if differencing:
          #differencing the data
          for col in df.columns:
            train.loc[:, col] = train[col].diff()
            test.loc[:, col] = test[col].diff()

        train = train.dropna()
        test = test.dropna()
        return train , test

    def frame_myseries(self, X ,lags):
      exo = self.exo
      if  exo is not None:
        Y = X.drop(exo , axis = 1 )

      else:
        Y = X

      X_train, X_val, y_train, y_val = train_test_split(X, Y, train_size= 0.8, random_state=42, shuffle= False)

      Xs = []
      Ys = []
      data = []
      target = []
      frames_list1 = [X_train , X_val]
      frames_list2 = [y_train , y_val]

      #if exogenous variables are present

      for X in  frames_list1:
        for i in range(lags, len(X) ):
          data.append(X.iloc[i-lags:i].values.flatten())
        Xs.append(data)
        data = []

      for Y in frames_list2:
        for i in range(lags, len(Y)):
          target.append(Y.iloc[i].values.flatten())
        Ys.append(target)
        target = []

      X_train, X_val =  np.array(Xs[0]) , np.array(Xs[1])
      y_train , y_val = np.array(Ys[0]) , np.array(Ys[1])
      # Convert to PyTorch tensors
      X_train = torch.from_numpy(X_train).float()
      y_train = torch.from_numpy(y_train).float()
      X_val = torch.from_numpy(X_val).float()
      y_val = torch.from_numpy(y_val).float()

      return X_train , X_val , y_train , y_val


    def get_myloaders(self, batch_size: int):
        '''
        Preprocess and frame the dataset
        :param batch_size: batch size
        :return: DataLoaders associated to training and testing data
        '''
        #transformations
        data_train, data_test= self.preprocess_mydata() #train-test split and the standardization process.

        #sliding window technique for supervised learning
        X_train, X_val, y_train , y_val = self.frame_myseries(data_train, self.lags )
        #print('X_train: ' , X_train.shape)
        #print('X_val: ' , X_val.shape)
        #print('y_train: ' , y_train.shape)
        #print('y_val: ' , y_val.shape)
        train_dataset = TensorDataset(X_train , y_train)
        test_dataset = TensorDataset(X_val , y_val)

        #make batches
        train_iter = DataLoader(train_dataset, batch_size=batch_size, shuffle=False, drop_last=False)
        val_iter = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, drop_last=False)
        return train_iter, val_iter, data_test

# #load the data
# data = pd.read_csv('mvtseries.csv')
# data = data.drop('Unnamed: 0' , axis = 1)

# #instantiate
# datset = MyTimeSeriesDataset(df= data, lags = 2, horizon_length = 2 , standardise = False , differencing = False , exo = None)

# # # Get data loaders
# train_loader, val_loader, test_data = datset.get_myloaders(batch_size=1)
# for i, (inputs, labels) in enumerate(train_loader):
#     print(f'Batch {i + 1}')
#     print('Inputs:', inputs)
#     print('Labels:', labels)
#     print('Input shape:', inputs.shape)
#     print('Label shape:', labels.shape)
#     print('-' * 20)



# # Print outputs
# print("Train Loader:")
# for batch in train_loader:
#     print(batch)
#     break  # Just print the first batch for brevity
# #

#train , test = datset.preprocess_mydata()
#X_train , X_val, y_train , y_val= datset.frame_myseries(train , 2)

#data.iloc[ 402: 407 , :]

#X_train

#X_val[0]

#y_train[-1]

#y_val[-1]
#X_val[-1 , :]

# data.iloc[ -5: , :]

#test

#test

#data.iloc[ -5: , :]