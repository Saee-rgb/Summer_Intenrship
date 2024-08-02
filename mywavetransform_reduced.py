# -*- coding: utf-8 -*-
"""mywavetransform_reduced.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JqVWpJ5VbhP2G_7LpPXFFbbMDcyAikrk
"""

!pip install properscoring

from modwt import modwt, imodwt
import pandas as pd
import numpy as np
import bredvarnet_latest_function
import mytsdataset_latest

from bredvarnet_latest_function import BRedVARNet
from mytsdataset_latest import MyTimeSeriesDataset

def mywavetransform(df ,
                    exo_test,
                    wname = 'haar',
                    lev = 4,
                    horizon_length = 4,
                    lags = 2,
                    exo = None,
                    diff = False,
                    std = False):

  #############
  ## Subset
  ##############
  colnames = df.columns
  if exo is not None:
    df_exo = df[exo]
    df_endo = df.drop(columns = exo)
    d = len(df_endo.columns)
  else:
    df_endo = df
    d = len(df_endo.columns)

  ######################
  ###MODWT Transform
  ######################
  wt_transforms = []
  for col in df_endo.columns[0:]: #this part is fishy : are we including the 0th indexed variable?
    df_endo[col] = df_endo[col].astype(float)
    wt = modwt(df_endo[col], wname, lev)
    wt_transforms.append(wt)
  #print("wavelet trasnform coeff shape : " ,  wt_transforms[0].shape ,'\n')

  wt_df_list = []
  for i in range(len(wt_transforms)):
    wt_df = pd.DataFrame(wt_transforms[i])
    wt_df = wt_df.transpose()
    wt_df_list.append(wt_df)

  #############################
  ###Collecting Decompositions
  ##############################

  #COllect the decomposition of each level for every variable in separate dfs
  separate_dfs = []
  # Iterate over each index position
  for index in range(len(wt_transforms[0])):
    df_columns = []
    #iterate over each dataframe
    for df in wt_df_list:
        df_columns.append(df[index])  # Append the column at the current index position
    separate_dfs.append(pd.concat(df_columns, axis=1))

  #print('before forecasting df shape : ' , separate_dfs[0].shape)


  #############################
  ###Forecasting
  #############################
   ##Make forecasts with BRedVARNet including the exogenous variables
  forecasts_list = []

  ##If exogenous variables are present, following chunk is executed
  newseparate_dfs = []
  if exo is not None:
    for df in separate_dfs:
      foo = [df , df_exo]
      df = pd.concat(foo, axis = 1)
      newseparate_dfs.append(df)
  else:
    newseparate_dfs = separate_dfs

 ##Fit BRedVARNet and forecast!
  #print('before forecasting df shape : ' , newseparate_dfs[0].shape)
  #print('column names before forecasting' , newseparate_dfs[0].columns)

  for dframe in newseparate_dfs:
    dframe.columns = colnames
    #print('dframe shape : ' , dframe.shape)
    #print('dframe col names : ' , dframe.columns)
    forecasts_df = BRedVARNet(dframe, exo_test = exo_test ,standardise=std,
                              differencing=diff , exo = exo , lags = lags , m_steps=horizon_length )
    forecasts_list.append(forecasts_df)
    #print('after forecasts shape: ' , forecasts_df.shape)
    #print('after forecasts col names: ' , forecasts_df.columns)

  ##############################
  ##Taking inverse of modwt
  ##############################
  inverse_forecasts_list = []
  for df in forecasts_list:
    inverse_df = pd.DataFrame()
    for i in range(len(df.columns)):
        col = df.iloc[: , i].to_numpy()
        col_list = [col]
        inverse_col = imodwt(col_list, wname)
        inverse_df[df.columns[i]] = inverse_col
        inverse_forecasts_list.append(inverse_df)

  ##################################
  #####Getting ensemble of forecasts
  ####################################
  concatenated_array = np.concatenate(inverse_forecasts_list, axis=1)
  df_concat = pd.DataFrame(concatenated_array)

  final_forecasts = []
  for i in range(len(wt_transforms)):
    dfnew = df_concat.iloc[ : , i : (i+ d)] #replace 6 by no of endogenous variables in df
    final_forecasts.append(dfnew)
  return final_forecasts

def addframes(dflist):
    sumframe = np.zeros(dflist[0].shape)
    for dataframe in dflist:
        dataframe = dataframe.to_numpy()
        sumframe =  sumframe+ dataframe
    return pd.DataFrame(sumframe)