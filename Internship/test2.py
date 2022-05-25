from operator import index
import yfinance as yf
import numpy as np 
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
yf.pdr_override() 
import datetime as dt 
from sklearn.cluster import KMeans
from functools import reduce
from dateutil.relativedelta import relativedelta
from A_Kmeans import main as A_kmeanslist
from B_Momentum import main as B_Momentum
plt.style.use('fivethirtyeight')




def portfopt (model):
#With this function the user will decide between the two models available 'Kmeans', and  'Momentum'
    if model == 'Kmeans':
        A_kmeanslist(market, start , end, optimization))
        assests_list = A_kmeanslist
    elif model == 'Momentum':
        assests_list = B_Momentum
    return assests_list

def getdata_opt_port(tickers,start,end):

#load the data in one DataFrame
    ind_data = pd.DataFrame()
    for t in tickers:
        ind_data[t] = pdr.DataReader(t,data_source='yahoo', start= start, end =end )['Adj Close']
    
    #ind_data.to_csv('sample6.csv')
    return ind_data 


def total_opt(data):  
    
#Covariance and Correlation matrix
    #data['Date'] = pd.to_datetime(data['Date']) # Change this for production
    #data = data.set_index('Date') #change this for production
    cov_matrix = data.astype(float).pct_change().apply(lambda x: np.log(1+x)).cov()   
   # return cov_matrix

#Covariance measures the directional relationship between the returns on two assets.

#def corr_matrix(data):
#The correlation matrix indicates in which way one asset moves given the change of the other asset.
#the correlation number is between -1 and 1,
# When the number is close to 1 the relationship is positive strong.
# When the number is close to -1 the relationship is negative strong.  
# When the number is close to 0 the relationship is null. 
    #corr_matrix = data.pct_change().apply(lambda x: np.log(1+x)).corr()
   # return corr_matrix

    
    
    
    ind_er = data.resample('M').last().pct_change().mean()

#def weights (data):
# With this function users can create a virtual weight for every single asset
    '''a=[]
    i=0
    for i in data.columns:
        i = + 1 
        b = i/(len(data.columns))
        a.append(b)
    w = dict(zip(data.columns, a))

    w = list(w(data).items())'''
    #method1 = [x[1] for x in w][:-1]
    #port_er = (method1 *ind_er).sum()

    sd = data.astype(float).pct_change().apply(lambda x: np.log(1+x)).std().apply(lambda x: x*np.sqrt(24))

                            
    assets = pd.concat([ind_er,sd], axis=1) 
    assets.columns = ['Returns', 'Volatility']

    #We create a loop to check all the possible combinations. 

#run loop 
    p_ret = [] # Define an empty array for portfolio returns
    p_vol = [] # Define an empty array for portfolio volatility
    p_weights = [] # Define an empty array for asset weights

    
    
    
    
     
    num_assets = len(data.columns)
    num_portfolios = 10000
    np.random.seed(99)

    for portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights = weights/np.sum(weights)
        p_weights.append(weights)
        returns1 = np.dot(weights, ind_er) # Returns are the product of individual expected returns of asset and its weights

        p_ret.append(returns1)
        
       
        var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum() #Portfolio Variance
        sd = np.sqrt(var)#hour??? standard deviation
        ann_sd = sd*np.sqrt(24) # monthly standard deviation = volatility
        p_vol.append(ann_sd)

    

    data1 = {'Returns':p_ret, 'Volatility':p_vol}

    for counter, symbol in enumerate(data.columns.tolist()):
        #print(counter, symbol)
        data1[symbol+' weight'] = [w[counter] for w in p_weights]

    
      
    portfo  = pd.DataFrame(data1)
    
    #idxmin() gives us the minimum value in the column specified.  
    min_vol_port = portfo.iloc[portfo['Volatility'].idxmin()]

    rf = 0.001 #risk factor
    optimal_risky_port = portfo.iloc[((portfo['Returns']-rf)/portfo['Volatility']).idxmax()]

    portfo.plot.scatter(x='Volatility', y='Returns', marker='o', s=10, alpha=0.3, grid=True, figsize=[10,10])
    plt.title('Combination different portfolios')

    min_vol_port = portfo.iloc[portfo['Volatility'].idxmin()]
    
    rf = 0.001 #risk factor
    optimal_risky_port = portfo.iloc[((portfo['Returns']-rf)/portfo['Volatility']).idxmax()]
    a = optimal_risky_port[1], optimal_risky_port[0]
    plt.scatter(min_vol_port[1], min_vol_port[0], color='r', marker='*', s=500)
    plt.scatter(optimal_risky_port[1], optimal_risky_port[0], color='g', marker='*', s=500)
    plt.savefig('Portfolio Optimization')

    return [min_vol_port, optimal_risky_port, plt.savefig('Portfolio Optimization')]
    #return cov_matrix


'''if __name__ == '__main__':
    tickers = ['AXP', 'AAPL', 'CVX', 'HD', 'MSFT', 'UNH']
    
    result = portfopt(tickers)'''


if __name__=='__main__':

    data1 =pd.read_csv('sample0.csv') 
    result = total_opt(data1)
    
    print(result)




if __name__=='__main__':
    tickers =['AXP', 'AAPL', 'CVX', 'HD', 'MSFT', 'UNH']
#get prices for the dji for the last year
    start = dt.datetime(2021,3,31)
    end = dt.datetime(2022,3,31)
    dataframe  = getdata_opt_port(tickers,start,end)

    print(dataframe)