import os
import requests
import json

def upload_document(file_name, file_path):
    url = str(os.environ.get('BACKEND_URL')) + "/api/upload/uploadDocument"
    print("upload URL", url)
    payload = {}
    files = [
        ('documentFile', (file_name, open(file_path + file_name, 'rb'), 'text/csv'))
    ]
    headers = {}

    print(files)
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)
    response_dict = json.loads(response.text)
    inputdata = response_dict["data"]["documentFileUrl"]
    print(inputdata)
    return inputdata["original"]


def upload_image(file_name, file_path):
    url = str(os.environ.get('BACKEND_URL')) + "/api/upload/uploadImage"
    print("upload URL", url)
    payload = {}
    files = [
        ('imageFile', (file_name, open(file_path + file_name, 'rb'), 'image/png'))
    ]
    print(files)
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)
    response_dict = json.loads(response.text)
    print(response_dict["data"])
    inputdata = response_dict["data"]["imageFileURL"]
    print(inputdata)
    return inputdata["original"]


def save_results(file_name, file_path,datatype=None):
    """
    input:
        file_name: Name of the file
        File_path: location of the file
        Type: file type
            images ,CSV, Json, Txt
    """

    if datatype in ['str','int','float','dict','json']:
        return file_path
    elif datatype in ["image","graph"]:
        return upload_image(file_name, file_path)
    elif datatype in ["csv", "CSV", "txt"]:
        return upload_document(file_name, file_path)

    return file_path
