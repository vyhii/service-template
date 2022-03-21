import os, shutil
from Datashop.get_data import *
from Datashop.backend import save_results
from Datashop.post_process import updateJob

if (os.path.exists("tmp")):
    shutil.rmtree("tmp")
os.mkdir('tmp')