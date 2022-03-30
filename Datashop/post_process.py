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

    if (error):
        payload = json.dumps({
            "jobid": jobID,
            "insightFileURL": "N/A",
            "duration": str(duration)
        })
    else:
        payload = json.dumps({
            "jobid": jobID,
            "insightFileURL": str(insightsS3Link),
            "duration": str(duration)
        })


    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("PUT", dataShopEndpointURL, headers=headers, data=payload)
    status_map["json_response"] = json.dumps(response.text)
    status_map["status_code"] = response.status_code

    print("job updated : ",payload)
    print("status : ",response.text)
    return payload


def zip_output_files(fileLocationToZip):
    zip_file = "tmp/post-process/" + fileLocationToZip.split("/")[-1] + ".zip"

    with zipfile.ZipFile(zip_file, 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(fileLocationToZip):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, basename(filePath))

    print(f"Files zipped to : {zip_file}")

