import numpy as np
import io
import random
import tensorflow as tf
import glob
import os
import cv2
from model import model



def run(jobID):
  print("************************ \n\n excuting jobID:"+ str(jobID)+" \n\n\n")
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

  fileslist = glob.glob(os.getcwd()+"/tmp/"+jobID+"-image"+"*")

  #load image as numpy array
  img = cv2.imread(fileslist[0])
  img = cv2.resize(img, (224, 224))
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  img = np.expand_dims(img, axis=0)
  result  = model.predict(img)



  if result[0][0] > 0.5:
    result = {
      "Autistic": "Positive",
      "confidence":str(result[0][0])
    }

  else:
    result = {
      "Autistic": "Negative",
      "confidence": str(result[0][0])
    }
  print("model inference finished!", str(result))

  return [result]

if __name__ == "__main__":
  run("61ef72ed396fc5330c15f250")