import json
import requests
import zipfile
import os



def updateJob(jobID, insightsS3Link,duration, error=None):
    """
    title::
        __updateJob
    description::
        Update the dataapplication with insightsLink.
    inputs::
    jobID
       Job ID from datashop application.
    insightsS3Link
       Downloadable URL of the insights.

    returns::
    payloadforservice
        response from the datashop application.
    """

    status_map = {'status_code': '', 'json_response': ''}
    dataShopEndpointURL = os.environ.get('BACKEND_URL') + "/api/job/updateJob"

    print("job update API : ", dataShopEndpointURL)

    if (error):
        payload = json.dumps({
            "insightFileURL": "N/A",
            "jobid": jobID,
            "duration": duration
        })
    else:
        payload = json.dumps({
            "insightFileURL": insightsS3Link,
            "jobid": jobID,
            "duration": duration
        })

    print("payload : ", payload)

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("PUT", dataShopEndpointURL, headers=headers, data=payload)
    print("update job response : ", response.text)
    status_map["json_response"] = json.dumps(response.text)
    status_map["status_code"] = response.status_code

    print("job updated : ",payload)
    return payload


def zip_output_files(fileLocationToZip):
    zip_file = "tmp/post-process/" + fileLocationToZip.split("/")[-1] + ".zip"

    with zipfile.ZipFile(zip_file, 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(fileLocationToZip):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, basename(filePath))

    print(f"Files zipped to : {zip_file}")

