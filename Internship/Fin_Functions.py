import yfinance as yf
import numpy as np 
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
yf.pdr_override() 
import datetime as dt 
from sklearn.cluster import KMeans
from functools import reduce
from dateutil.relativedelta import relativedelta
plt.style.use('fivethirtyeight')
import io

def assets(market):
#With this function the user can pick between three different indexes 'DJI', 'S&P500' and 'ASX  and work with the model 
    if market == 'DJI':
        table = pd.read_html('https://www.investopedia.com/terms/d/djia.asp')[0]
        tickers = table[('Dow Jones Industrial Average Components',    'Symbol')].tolist()
    elif market == 'S&P500':
        table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
        tickers = table['Symbol'].tolist()
    elif market == 'ASX':
        table = pd.read_html('https://en.wikipedia.org/wiki/S%26P/ASX_200')[0]
        table['Code'][:3]
        tickers = []
        for asset in table['Code']:
            tickers.append(asset+'.AX')
    return tickers


def getdata_kmeans(tickers,start,end):

#load the data in one DataFrame
    ind_data = pd.DataFrame()
    for t in tickers:
        ind_data[t] = pdr.DataReader(t,data_source='yahoo', start= start, end =end )['Adj Close']
    print (ind_data.head())


#calculate the annual returns and variance
    daily_returns = ind_data.pct_change()
    annual_mean_returns = daily_returns.mean()*251
    annual_returns_variance = daily_returns.var()* 251

#create a new dataframe
    df = pd.DataFrame(ind_data.columns, columns = ['Stock Symbols'])
    df['Variances'] = annual_returns_variance.values
    df['Returns'] = annual_mean_returns.values

#Check if we have miss data 
    if df.isna().values.any().sum()> 0:
        check_missing = df.isnull()
        for column in check_missing.columns.values.tolist():
            df.dropna(axis = 0, inplace= True)
    
    return df


def plt_to_np(fig):
    with io.BytesIO() as buff:
        fig.savefig(buff, format='png')
        buff.seek(0)
        im =plt.imread(buff)
    return im

def elbow_method (data, random_state=99):

#Load the data 
    X= data[['Returns', 'Variances']].values
    inertia_list = []
    for k in range(2,25):

#create and train the model
        kmeans = KMeans(n_clusters = k, random_state=random_state)
        kmeans.fit(X)
        inertia_list.append(kmeans.inertia_)

#Plot the data
    f1 = plt.figure()
    plt.plot(range(2,25), inertia_list)
    plt.title('Elbow Curve')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia or Sum Squared Error(SSE)')
    #plot = plt.savefig('Elbow_plot')

    image = plt_to_np(plt)

    plot = {
        "elbow plot":image
    }

#Get and Show the labels / groups
    kmeans = KMeans(n_clusters = 5).fit(X)
    labels = kmeans.labels_

    data['Cluster_labels'] = labels

    return [plot , data]
    
    
def besteachclust (data):

#Find the best asset given each cluster
    c = []
    for i in range(0,5):
        a = data.loc[(data['Cluster_labels'] == i)].sort_values(by="Returns",ascending=False).index[0]
        c.append(a)
    dfa= data.loc[c, :]
    df2 = dfa.sort_values(by="Returns",ascending=False)
    df2['Cluster_legend']= ['Really good Positive Returns','Medium Returns', 'Acceptable Positive Returns','Close to zero Returns','Negative Returns']
    
# Merge information in one data set to be used after for plot
    legend = df2[['Cluster_labels','Cluster_legend']]
    legend.set_index('Cluster_labels')
    #test = leg.to_dict()
    test3 = pd.merge(data,legend, on ='Cluster_labels')
    test3.to_csv('sample3.csv', index=False)
    return test3
    
  
def plotall(data):
#Use the right information to plot the differents clusters

#Create the different dataframes for every case 
    legend = ['Really good Positive Returns','Medium Returns', 'Acceptable Positive Returns','Close to zero Returns','Negative Returns']

    Good_returns = data.loc[(data['Cluster_legend']== 'Really good Positive Returns')]
    Medium_Returns = data.loc[(data['Cluster_legend']== 'Medium Returns')]
    Acceptable_Returns = data.loc[(data['Cluster_legend']== 'Acceptable Positive Returns')]
    Closezero = data.loc[(data['Cluster_legend']== 'Close to zero Returns')]
    Negative_Returns = data.loc[(data['Cluster_legend']== 'Negative Returns')]

#Now we plot the  clusters    
    plt.figure(figsize=(9,9), dpi=80)

    colors = ['b', 'c', 'y', 'm', 'r']
    Good = plt.scatter(Good_returns['Returns'], Good_returns['Variances'],   marker='o', color=colors[0])
    Medium = plt.scatter(Medium_Returns['Returns'], Medium_Returns['Variances'], marker='o', color=colors[1])
    Acceptable  = plt.scatter(Acceptable_Returns['Returns'], Acceptable_Returns['Variances'], marker='o', color=colors[2])
    Close0  = plt.scatter(Closezero['Returns'], Closezero['Variances'], marker='o', color=colors[3])
    Negative  = plt.scatter(Negative_Returns['Returns'], Negative_Returns['Variances'], marker='o', color=colors[4])


    plt.title('K-means plot')
    plt.xlabel('Returns')
    plt.ylabel('Variances')
    plt.legend((Good, Medium, Acceptable, Close0, Negative),
           ('Really good Positive Returns','Medium Returns', 'Acceptable Positive Returns','Close to zero Returns','Negative Returns'),
           loc='upper right')

    plot = plt.savefig('K-means Plot')
    return plot



def diversed_port(data):
#Create a diversify portfolio with only the two best performances on each cluster
    symbol=[]
    for i in range (0,5):
        a = data[data['Cluster_labels']==i].sort_values(by="Returns",ascending=False)
        a = a[a['Cluster_labels']==i]['Stock Symbols'][:2].tolist()
        symbol.append(a)
        single_list = reduce(lambda x,y: x+y, symbol)
    return single_list

def portfolios(data ,leg = 'Really good Positive Returns' ):
#Create a portfolio given one of the five legends
# The legends are  'Really good Positive Returns','Medium Returns', 'Acceptable Positive Returns','Close to zero Returns','Negative Returns'
    a = data.loc[(data['Cluster_legend'] == leg )].sort_values(by="Returns",ascending=False)
    a = a['Stock Symbols'].tolist()
    return a

def getdata_momentum(tickers,start,end):

#load the data in one DataFrame
    ind_data = pd.DataFrame()
    for t in tickers:
        ind_data[t] = pdr.DataReader(t,data_source='yahoo', start= start, end =end )['Adj Close']
    print (ind_data.head())

#calculate the monthly returns and variance
    mtl_ret = ind_data.pct_change().resample('M').agg(lambda x:(x+1).prod()-1)

#calculate returns over the past 11 months
    past_11 = (mtl_ret+1).rolling(11).apply(np.prod)-1

    index_list = [i for i, item in enumerate(past_11.index)]

    reference_dict = dict(zip(index_list, past_11.index))

    for key in reference_dict.keys():
        key, reference_dict[key]

    """In this part we can see the returns during the study time period. """

    formation = reference_dict[len(reference_dict)-2]
    print (formation)

#loop through reference_dict, match with formation
    for key in reference_dict.keys():
        if formation == reference_dict[key]:
            previous_month = reference_dict[key-1]

    index_list = [i for i, item in enumerate(past_11.index)]

    reference_dict = dict(zip(index_list, past_11.index))

    for key in reference_dict.keys():
        key, reference_dict[key]

    ret_12 = past_11.loc[previous_month]  

    ret_12 = ret_12.reset_index() 
#Get the Database wuth the respective quintiles 
    ret_12['quintile'] = pd.qcut(ret_12.iloc[:,1],5,labels=False)

    return ret_12        

def get_quintiles(data, quintil):
#With this Function the user will be able to identitify the different quintiles in the model just need to assign the number 
  #group = pd.DataFrame()
  group = data[data.quintile==quintil]['index'].sort_values(ascending=False).tolist()[:5]

  return print(group)

'''def portfopt (market):
#With this function the user will decide between the two models available 'Kmeans', and  'Momentum'
    if market == 'Kmeans':
        assests_list = A_Kmeans.a 
    elif market == 'Momentum':
        assests_list = get_quintiles(data,quintil)
    return assests_list

def optipro(data):  
#Covariance and Correlation matrix
    cov_matrix = data.pct_change().apply(lambda x: np.log(1+x)).cov()   
#Covariance measures the directional relationship between the returns on two assets.
#The correlation matrix indicates in which way one asset moves given the change of the other asset.
#the correlation number is between -1 and 1,
# When the number is close to 1 the relationship is positive strong.
# When the number is close to -1 the relationship is negative strong.  
# When the number is close to 0 the relationship is null. 
    #corr_matrix = data.pct_change().apply(lambda x: np.log(1+x)).corr()

    a=[]
    i=0
    for i in data.columns:
        i = + 1 
        b = i/(len(data.columns))
        a.append(b)
    w = dict(zip(data.columns, a))

    #port_var = cov_matrix.mul(w, axis=0).mul(w, axis=1).sum().sum()
    # monthly returns for individual companies
    ind_er = data.resample('m').last().pct_change().mean()
    #Portfolio returns
    #port_er = (a*ind_er).sum()

    # Volatility is given by the monthly standard deviation. We multiply by 24 because there are 24 trading days/month.
    mtl_sd = data.pct_change().apply(lambda x: np.log(1+x)).std().apply(lambda x: x*np.sqrt(24))

    # Creating a table for visualising returns and volatility of assets
    assets = pd.concat([ind_er, mtl_sd], axis=1) 
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
        returns = np.dot(weights, ind_er) # Returns are the product of individual expected returns of asset and its weights

        p_ret.append(returns)
        var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum() #Portfolio Variance
        sd = np.sqrt(var)#hour??? standard deviation
        ann_sd = sd*np.sqrt(24) # monthly standard deviation = volatility
        p_vol.append(ann_sd)
# We gather all the results
    data1 = {'Returns':p_ret, 'Volatility':p_vol}

    for counter, symbol in enumerate(data.columns.tolist()):
        #print(counter, symbol)
        data1[symbol+' weight'] = [w[counter] for w in p_weights]
    optportfolios  = pd.DataFrame(data1)

    optportfolios.plot.scatter(x='Volatility', y='Returns', marker='o', s=10, alpha=0.3, grid=True, figsize=[10,10])
    min_vol_port = optportfolios.iloc[optportfolios['Volatility'].idxmin()]
    plt.scatter(min_vol_port[1], min_vol_port[0], color='r', marker='*', s=500)
    plt.title('Combination different portfolios')
    rf = 0.001 # risk factor
    optimal_risky_port = optportfolios.iloc[((optportfolios['Returns']-rf)/optportfolios['Volatility']).idxmax()]
    plt.scatter(optimal_risky_port[1], optimal_risky_port[0], color='g', marker='*', s=500)
    plot = plt.savefig('Optimization Plot')
    return [min_vol_port , optimal_risky_port]

    

    #Frustation, array in np i can not use the labels for the plot, k means change the number of the assets therefore not sure how to determine the best, struggling finding how to save the pic (save but it looks not nice)
    #Next iteration plot with labels and organize the table and identify the best performance assets
    #from momentum and kmeans to optimization how to take the data


if __name__=='__main__':
    data =pd.read_csv('sample0.csv')
    result = optipro(data)
    
    print(result)


if __name__=='__main__':
  market ='Kmeans'
  result = portfopt(market)
  print(result) '''



if __name__=='__main__':
  market ='DJI'
  tickers = assets(market)
  print(tickers)    
    


if __name__=='__main__':
    tickers
#get prices for the dji for the last year
    start = dt.datetime(2021,3,31)
    end = dt.datetime(2022,3,31)
    dataframe  = getdata_kmeans(tickers,start,end)

    print(dataframe)



if __name__=='__main__':
    data = pd.read_csv('sample1.csv')
    result = elbow_method(data)

    print(result)


if __name__=='__main__':
    data1 = pd.read_csv('sample2.csv')
    result = besteachclust(data1)

    print(result)
    
    
if __name__=='__main__':
    data1 = pd.read_csv('sample3.csv')
    result = plotall(data1) 

    print(result)

if __name__=='__main__':
    data1 = pd.read_csv('sample2.csv')
    result = diversed_port(data1) 

    print(result)


if __name__=='__main__':
    data1 = pd.read_csv('sample3.csv')
    result = portfolios(data1, 'Really good Positive Returns') 

    print(result)

if __name__=='__main__':
    tickers
    start = dt.datetime(2021,3,31)
    end = dt.datetime(2022,3,31)
    dataframe  = getdata_momentum(tickers,start,end)
    dataframe.to_csv('samplemomentum.csv' )

    print(dataframe)

if __name__=='__main__':
    data = pd.read_csv('samplemomentum.csv')
    quintil =1
    lista = get_quintiles(data, quintil)

    print(lista)

'''functio
    3 inputs
    list of compacny
    process the list
    get data from yahoo for the list


    cal mean / deference
    put it in da dataframe
    return the data frame'''
