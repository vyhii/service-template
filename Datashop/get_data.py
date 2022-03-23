import requests
import zipfile
import json

"""
    title:: pre_process
    description:: takes dataset URL and jobID as input, download the dataset and read the input.

"""

def extract_zip_file(zipped_file):
    """
    title::
        extract_zip_file
    description::
        extract the files in the zip file.
    inputs::
        zipped_file
             URL for the downloaded zipfile.
    returns::
         extracted_folder
              extracted zip files
    """

    extracted_folder = "tmp/" + zipped_file.split("/")[-1].replace(".zip", "") + "/"
    with zipfile.ZipFile(zipped_file, 'r') as zip_ref:
        zip_ref.extractall(extracted_folder)
    print(f"Files extracted to {extracted_folder}")
    print(f"list of filenames:  {zip_ref.namelist()}")

    return extracted_folder, zip_ref.namelist()


def downloadFile(jobID, url):

    fileextention = url.split(".")[-1]

    if fileextention == "jpeg" or "jpg" or "png":
        filetype = "image"
    elif fileextention == "csv":
        filetype = "csv"
    elif fileextention == "mp4" or "mkv" or "mpeg":
        filetype = "video"
    elif fileextention == "zip" or "tar.gz" or "gz":
        filetype = "compressed"
    else:
        filetype = "other"

    input_file_location = f"tmp/{jobID}-{filetype}.{fileextention}"

    req = requests.get(url)

    with open(input_file_location, 'wb') as fileHandle:
        fileHandle.write(req.content)
    print(f"File Downloaded to {input_file_location}")

    return input_file_location, fileextention




def get_data(jobID, inputdata):
    """
    title::
        run
    description::
        takes dataset URL and jobID as input, download the dataset and read the input
    inputs::
    jobID
       Job ID from datashop application
    url
       Downloadable URL of the dataset
    json1
       json data from the model.

    returns::
    payloadforservice
        payload for model/service

    """
    url = inputdata["url"]
    json1 =inputdata["json"]


    if ((json1 == '') and (url == '')):
        print("No data recieved")
        return

    if (json1 != ''):
        data = json1['body']
        with open('tmp/data.json','w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    if (url != ''):
        input_file_location, fileName = downloadFile(jobID, url)
        if fileName.endswith(".zip"):
            extract_zip_file(input_file_location)


if __name__ == '__main__':

    id = ""
    url = ""
    json_string = {'body' : {
    "Gender": "female",
    "TotalHeight": 1715,
    "Inseam": 845,
    "Bust": 880,
    "UnderBust": 780,
    "Waist": 721,
    "HighHip": 770,
    "LowHip": 865,
    "HighThigh": 491,
    "LowThigh": 417,
    "NeckBase": 460,
    "Suitleglength": 190
    }}

    #get_data(id,url,json_string)

    #print(downloadFile("12344", "https://data-shop-backend.s3.ap-southeast-2.amazonaws.com/files/docs/original/Docs_dupcuvPvgAEv.tar.gz"))