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

plt.style.use('fivethirtyeight')




'''def portfopt (market):
#With this function the user will decide between the two models available 'Kmeans', and  'Momentum'
    if market == 'Kmeans':
        assests_list = A_Kmeans.a 
    elif market == 'Momentum':
        assests_list = get_quintiles(data,quintil)
    return assests_list'''



def cov_matrix(data):  
#Covariance and Correlation matrix
    cov_matrix = data.pct_change().apply(lambda x: np.log(1+x)).cov()   
    return cov_matrix

#Covariance measures the directional relationship between the returns on two assets.

def corr_matrix(data):
#The correlation matrix indicates in which way one asset moves given the change of the other asset.
#the correlation number is between -1 and 1,
# When the number is close to 1 the relationship is positive strong.
# When the number is close to -1 the relationship is negative strong.  
# When the number is close to 0 the relationship is null. 
    corr_matrix = data.pct_change().apply(lambda x: np.log(1+x)).corr()
    return corr_matrix


def weights (data):
# With this function users can create a virtual weight for every single asset
    a=[]
    i=0
    for i in data.columns:
        i = + 1 
        b = i/(len(data.columns))
        a.append(b)
    w = dict(zip(data.columns, a))

    return w

def port_ind_exp(data):
# Monthly returns for individual companies
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.set_index('Date')
    ind_er = data.resample('M').last().pct_change().mean()
    return ind_er

def port_returns(data):
#Returns for the portfolio total
    w = list(weights(data).items())
    method1 = [x[1] for x in w][:-1]
    port_er = (method1 *port_ind_exp(data)).sum()

    return port_er

def mtl_Std(data):
# Volatility is given by the monthly standard deviation. We multiply by 24 because there are 24 trading days/month.
    sd = data.astype(float).pct_change().apply(lambda x: np.log(1+x)).std().apply(lambda x: x*np.sqrt(24))
    return sd

def assets_table (data):
# Creating a table for visualising returns and volatility of assets
    
    a = port_ind_exp(data)  
    b = mtl_Std(data.iloc[:, 1:])
                            
    assets = pd.concat([a,b], axis=1) 
    assets.columns = ['Returns', 'Volatility']
    
    return  assets

def portfolioss(data):
#We create a loop to check all the possible combinations. 

#run loop 
    p_ret = [] # Define an empty array for portfolio returns
    p_vol = [] # Define an empty array for portfolio volatility
    p_weights = [] # Define an empty array for asset weights

    
    
    
    
    b = cov_matrix(data.iloc[:, 1:]) 
    num_assets = len(data.columns[1:])
    num_portfolios = 10000
    np.random.seed(99)

    for portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights = weights/np.sum(weights)
        p_weights.append(weights)
        a = port_ind_exp(data)
        returns1 = np.dot(weights, a) # Returns are the product of individual expected returns of asset and its weights

        p_ret.append(returns1)
        
       
        var = b.mul(weights, axis=0).mul(weights, axis=1).sum().sum() #Portfolio Variance
        sd = np.sqrt(var)#hour??? standard deviation
        ann_sd = sd*np.sqrt(24) # monthly standard deviation = volatility
        p_vol.append(ann_sd)

    a = pd.DataFrame(data)
    a = a.set_index('Date')

    data = {'Returns':p_ret, 'Volatility':p_vol}

    for counter, symbol in enumerate(a.columns.tolist()):
        #print(counter, symbol)
        data[symbol+' weight'] = [w[counter] for w in p_weights]

    
      
    portfolioss  = pd.DataFrame(data)
    
    
    return portfolioss

def min_portfolio(data1):
#idxmin() gives us the minimum value in the column specified.  
    min_vol_port = data1.iloc[data1['Volatility'].idxmin()]
                             
    return min_vol_port

def optimal_risk(data1):
    rf = 0.001 #risk factor
    optimal_risky_port = data1.iloc[((data1['Returns']-rf)/data1['Volatility']).idxmax()]

    return optimal_risky_port


def plot_portfolios(data1):

    data1.plot.scatter(x='Volatility', y='Returns', marker='o', s=10, alpha=0.3, grid=True, figsize=[10,10])
    plt.title('Combination different portfolios')

    min_vol_port = data1.iloc[data1['Volatility'].idxmin()]
    #plt.subplots(figsize=(10, 10))
    rf = 0.001 #risk factor
    optimal_risky_port = data1.iloc[((data1['Returns']-rf)/data1['Volatility']).idxmax()]
    a = optimal_risky_port[1], optimal_risky_port[0]
    plt.scatter(min_vol_port[1], min_vol_port[0], color='r', marker='*', s=500)
    plt.scatter(optimal_risky_port[1], optimal_risky_port[0], color='g', marker='*', s=500)
    
    
    return plt.savefig('Portfolio Optimization')
    

if __name__=='__main__':

    data1 =pd.read_csv('sample0.csv', index_col='Date')
    result = cov_matrix(data1)
    
    print(result)
 

if __name__=='__main__':

    data1 =pd.read_csv('sample0.csv',index_col='Date')
    result = corr_matrix(data1)
    
    print(result)

if __name__=='__main__':

    data =pd.read_csv('sample0.csv',index_col='Date')
    result = weights(data)
    
    print(result)

if __name__=='__main__':

    data =pd.read_csv('sample0.csv')
    result = port_ind_exp(data)

    print(result)





if __name__=='__main__':

    data =pd.read_csv('sample0.csv')
    result = port_returns(data)

    print(result)

if __name__=='__main__':

    data =pd.read_csv('sample0.csv',index_col='Date')
    result = mtl_Std(data)

    print(result)

if __name__=='__main__':

    data =pd.read_csv('sample0.csv')
    result = assets_table(data)

    print(result)

if __name__=='__main__':

    data =pd.read_csv('sample0.csv')
    result = portfolioss(data)
    
    print(result)

if __name__=='__main__':

    data =pd.read_csv('sample5.csv')
    result = min_portfolio(data)
    
    print(result)

if __name__=='__main__':

    data =pd.read_csv('sample5.csv')
    result = optimal_risk(data)
    
    print(result)

if __name__=='__main__':

    data =pd.read_csv('sample5.csv')
    result = plot_portfolios(data)
    
    print(result)


