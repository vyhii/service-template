import numpy as np
import io
import random

def run(jobID):
  """
  title:: 
      run
  description:: 
      Run the model/get the predictions according the service.
  inputs::
      jobID 
            Job ID from datashop application used for search file or save file

  returns::
      insightsDataFileLocation
      insights data file location.

  load data from temp folder
    >  json data is data.json
    >  all images and CSV are named with jobID_"filetype"
    >  jobiD_csv.csv   "61ef72ed396fc5330c15f250_csv.csv"
    >  jobiD_image.png   "61ef72ed396fc5330c15f250_image.png"
  """

  #default data path
  datapath = "tmp/"

  ## perform model inference
  result_1 = random.random()

  print("model inference finished!",result_1)


  ## for multiple results return list of resutls   results = [result_1,result_2,result_3]

  return [str(result_1), str(random.random()), str(random.random()),str(random.random())]
