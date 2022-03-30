import os
import numpy as np
import io
import random
import glob
import cv2
from model import model

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
  # load data as list from temp folder

  fileslist = glob.glob(os.getcwd() + "/tmp/" + jobID + "-image"+"*")

  ## perform model inference

  img = cv2.imread(fileslist[0])
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  img = cv2.resize(img, (224, 224))
  img = np.expand_dims(img, axis=0)

  # run model
  result = model.predict(img)

  if result[0][0] > 0.5:
    result = {
      "Autistic": "Positive",
      "confidence": str(result[0][0] * 100)
    }

  else:
    result = {
      "Autistic": "Negative",
      "confidence": str(result[0][1] * 100)
    }
  print("model inference finished!", str(result))

  ## for multiple results return list of resutls   results = [result_1,result_2,result_3]

  return [result]
