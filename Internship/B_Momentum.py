from pandas_datareader import Options
import Fin_Functions
import datetime as dt

userinput = {
        "start" : dt.datetime(2021,1,1),
        "end" : dt.datetime(2022,4,4),
        "market": "DJI",
        "quintil": 4
        
    }
def main(market, start, end, quintil):

    #Define the market 
    # Options 'DJI', 'S&P500' and 'ASX'
    market = Fin_Functions.assets ('DJI')

    # Define the time to evaluate   
    start = dt.datetime(2021,1,1)
    end = dt.datetime(2022,4,4)

    #Extract the data and organize in relevance
    data = Fin_Functions.getdata_momentum(market,start,end)

    #Extract the 5 more important assets giving the quintile the user is interested. 
    # The user can pick the best quintil = 4 or the worst quintil = 0, or any other quintil 3,2,1  
    Result_momentum = Fin_Functions.get_quintiles(data, quintil)

    outputs = {

            "Result Momentum " :  Result_momentum 

        }
    return print(outputs)


if __name__=='__main__':
    #Define the market 
    # Options 'DJI', 'S&P500' and 'ASX'
    market = Fin_Functions.assets (userinput["market"])
    #Define the time
    start = userinput['start']
    end = userinput['end']
    #Define quintil
    quintil = userinput["quintil"]

    Result_momentum = main(market, start , end, quintil)
    
