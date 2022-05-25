# -*- coding: utf-8 -*-
"""Test502.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1S5qh7uQ3zO5FPzTPM7btHLT7es2tZV18

# Step 4: Buy in the right time
"""

# We installed the neccesary libraries to run the program
import yfinance as yf
import numpy as np 
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plts
yf.pdr_override() 
import datetime as dt 
from dateutil.relativedelta import relativedelta

#Get tiickers symbols the DJI
table = pd.read_html('https://www.investopedia.com/terms/d/djia.asp')[0]
table.columns

#tick = table[('Dow Jones Industrial Average Components',    'Symbol')].tolist()
tick = ['CSCO', 'KO', 'DOW', 'GS', 'HD', 'IBM']#, 'JNJ', 'MCD', 'MRK', 'NKE','PG', 'CRM', 'TRV', 'V', 'WMT']

#get prices for the dji for the last year
start = dt.datetime(2021,3,31)
#start1 = dt.datetime(2021,3,21)
end = dt.datetime(2022,3,31)

#load the data in one DataFrame
ind_data = pd.DataFrame()
for t in tick:
  ind_data[t] = pdr.DataReader(t,data_source='yahoo', start= start, end =end )['Adj Close']
print (ind_data.head())

df = pd.DataFrame(ind_data['CSCO'])
df.head(3)

#visually show the stock price
plt.figure(figsize = (12.2,4.5))
plt.plot(df, label = 'Close')
plt.title ('Close Price History')
plt.xlabel('Date')
plt.ylabel('Price in USD ($)')

#Calculate the MACD and signal line indicators
#Calculate the short term exponential moving average (EMA)
shortEMA = df.ewm(span=25,adjust=False).mean()#12
#Calculate the long term exponential moving average (EMA)
longEMA = df.ewm(span=50,adjust =False).mean()#26
#Calculate the MACD line
MACD = shortEMA - longEMA
#Calculate the signal line
signal = MACD.ewm(span=100,adjust=False).mean()#9

#Plot the chart
plt.figure(figsize=(12.2, 4.5))
plt.plot(df.index, MACD, label='KO-MACD', color= 'red')
plt.plot(df.index, signal, label='Signal Line', color = 'blue')
plt.legend(loc='upper right')
plt.show

#Create new columns for the data
df['MACD'] = MACD
df['signal line']= signal
#show the data
df

#Create a function to signal to buy and sell an asset
def buy_sell(signal):
  Buy=[]
  Sell=[]
  flag= -1

  for i in range(0,len(signal)):
    if signal['MACD'][i]> signal['signal line'][i]:
      Sell.append(np.nan)
      if flag !=1:
        Buy.append(signal['CSCO'][i])
        flag = 1
      else:
        Buy.append(np.nan)
    elif signal['MACD'][i] < signal['signal line'][i]:
      Buy.append(np.nan)
      if flag !=0:
        Sell.append(signal['CSCO'][i])
        flag = 0
      else:
        Sell.append(np.nan)
    else:
      Buy.append(np.nan)
      Sell.append(np.nan)
  return(Buy,Sell)

#Create buy and sell Column
a= buy_sell(df)
df['Buy_Signal_price']= a[0]
df['Sell_Signal_price']= a[1]

#Show the data
df.head(5)

#Visualy show the stock buy and sell signals
plt.figure(figsize=(12.2, 4.5))
plt.scatter(df.index, df['Buy_Signal_price'],color = 'green',label='Buy', marker='^', alpha = 1)
plt.scatter(df.index, df['Sell_Signal_price'],color = 'red',label='Sell', marker='v', alpha = 1)
plt.plot(df['CSCO'], label='Close Price', alpha = 0.35)
plt.title('close Price Buy & Sell Signals')
plt.xlabel('Date')
plt.ylabel('Close Price USD ($)')
plt.legend(loc='upper left')
plt.show