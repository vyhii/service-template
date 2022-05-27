import os, shutil
from Datashop.get_data import *
from Datashop.backend import save_results
from Datashop.post_process import updateJob
import requests
import time

if (os.path.exists("tmp")):
    shutil.rmtree("tmp")
os.mkdir('tmp')

def initialize(input_dict):
    """
    This function is used to initialize the phase 1 of the Datashop.
    """

    os.environ["BACKEND_URL"] = input_dict["datashopServerAddress"]

    inputdata = input_dict["dataFileURL"]
    jobID = input_dict["jobID"]

    # notify the Datashop application that job is in "Running" state
    updateJob(jobID, "running", None)

    # download userinput data and save in "tmp" folder
    get_data(jobID, inputdata)

    return jobID
