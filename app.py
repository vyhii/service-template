from flask import Flask, request, after_this_request
from flask_restful import Resource, Api
import service
import os, shutil
import time
import Datashop

app = Flask(__name__)
api = Api(app)

class predict(Resource):
    @staticmethod
    def post():
        try:
            start = time.time()

            input_dict = request.get_json()

            # phase 1 Datashop initialization
            jobID = Datashop.initialize(input_dict)

            # phase 2 calling the service
            service_results = service.run(jobID) # returns list of all the results

            # save results
            insightsS3Link = Datashop.save_results("filename", service_results[0], datatype="int")  #specify the dtype of result (image,csv,graph,json,str,int)

            # calculate job duration
            duration = time.time() - start

            # insightsS3Link can be a list of links [insightsS3Link1 ,insightsS3Link2 , insightsS3Link3]
            insights_payload = Datashop.updateJob(jobID,insightsS3Link,duration)

            return {"result": "success","duration":duration,"insightFileURL":insights_payload}
                        
        except Exception as e:
            # updating job with FAILED status.
            try:
                duration = time.time() -  start;
                Datashop.updateJob(jobID,None, duration , error= str(e))
                return {"result": "failed","duration":duration, "insightFileURL":str(e)}

            except Exception as e:
                duration = time.time() - start;
                return {"result": "update failed","duration": None, "insightFileURL":str(e)}



api.add_resource(predict,'/predict')

if __name__ == '__main__':
    app.run()


