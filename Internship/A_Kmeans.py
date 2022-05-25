from pickletools import optimize
from pandas_datareader import Options
import Fin_Functions
import datetime as dt

userinput = {
        "start" : dt.datetime(2021,1,1),
        "end" : dt.datetime(2022,4,4),
        "market": "DJI",
        "optimization": "Acceptable Positive Returns"
    }

def main(market, start, end):
    data = Fin_Functions.getdata_kmeans(market,start=start,end=end)

    #Run the model elbow method
    elbow_plot, data = Fin_Functions.elbow_method(data)
    image1 = Fin_Functions.plt_to_np(elbow_plot)



    #Define the best clusters
    data = Fin_Functions.besteachclust(data)

    #Plot all the assets 
    K_meansplot = Fin_Functions.plotall(data)
    image2 = Fin_Functions.plt_to_np(K_meansplot)

    #Diversified portfolio
    Diversified_portfolio = Fin_Functions.diversed_port(data)

    #Best Portfolio possible Options:
    #Really good Positive Returns','Medium Returns', 'Acceptable Positive Returns','Close to zero Returns','Negative Returns'
    Result_kmeans =Fin_Functions.portfolios(data,leg=userinput["optimization"])
    print(Result_kmeans)

    outputs = {

         "Diversified Port " :  Diversified_portfolio ,
         "optimization port": Result_kmeans,
         "elbow plot":image1,
         "K_means Plot": image2
    

     }

    return outputs




if __name__=='__main__':
    #Define the market 
    # Options 'DJI', 'S&P500' and 'ASX'
    trial = Fin_Functions.assets (userinput["market"])
    # Define the time to evaluate   
    start = userinput['start']
    end = userinput['end']
    leg = userinput["optimization"]
    #this is the starting point
    #main is the app / service

  

   


    

    Result_kmeans = main(trial, start , end)


