from pandas_datareader import Options
import Fin_Functions
import test2
import datetime as dt


#Define the portfolio
# The user can decided between 'Kmeans and Mommetum'
tick = test2.portfopt('Momentum')



# Define the time to evaluate   
start = dt.datetime(2021,1,1)
end = dt.datetime(2022,4,4)
data = test2.getdata_opt_port(tick,start=start,end=end)

# Define the neccesary functions to run the model and obtain the optimization portfolio

'''a = test1.cov_matrix(data, index_col='Date')
b = test1.corr_matrix(data, index_col='Date')
c= test1.weights (data, index_col='Date')

e = test1.port_returns(data)
d = test1.port_ind_exp(data)'''
f = test2.total_opt (data)
print(f[0])
print(f[1])




