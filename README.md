#Datashop service template


**Building a docker**

Include necessary packages for your model in requirements.txt. We prefer you to use pip freeze > requirements.txt 


**RUN Command to build DOCKER image**

To run the container 

```
docker build -d -t servicename .
```

**RUN Command to RUN DOCKER container**

```
docker run -d -p 5000:5000 servicename
```
