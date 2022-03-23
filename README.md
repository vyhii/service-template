# Datashop service template

## Overview

The main API is writen in app.py



service template is divided into three parts:

    * Phase 1 - To download the user uploaded data to "tmp" folder
    * Phase 2 - Service (ML model inference)
    * Phase 3 - Upload the results and update jobstatus to datashop applciation

Include necessary packages for your model in requirements.txt. We prefer you to use pip freeze > requirements.txt 
```angular2html
pip freeze > requirements.txt
```

**RUN Command to build DOCKER image**


```
docker build -d -t servicename .
```

**RUN Command to RUN DOCKER container**

```
docker run -d -p 5000:5000 servicename
```


## Test the service

Test your service by running thought postman

* Method : POST
* URL : http://localhost:5000/predict
* Body type: JSON

sample payload:
```angular2html
{
 "jobID" : "61ef72ed396fc5330c15f250",

 "dataFileURL":

     {

       "url": "",

       "json":""

     },
"datashopServerAddress": "http://34.129.168.181:8000"
}
```