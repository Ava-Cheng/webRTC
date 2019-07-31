# -*- coding: UTF-8 -*-
import os
import requests
import json
import time


def ckConnectionAndFile():
    # ping 8.8.8.8 Google的DNS
    confirm_connection = os.system('ping 8.8.8.8 -c 2')

    # 讀取json檔案寫進變數
    jsonFile = open("fileNotUploaded.json", 'r')
    jsonString = jsonFile.read()
    jsonFile.close()

    # 檢查連線
    # 檢查json檔案是否有檔案未上傳
    if confirm_connection or jsonString == "{}":
        t = time.time()
        while True:
            if time.time()-t > 30:
                ckConnectionAndFile()
            time.sleep(30)

    # 藉由讀檔獲取uuid
    jsonFile = open("fileNotUploaded.json", 'r')
    jsonString = jsonFile.read()
    jsonFile.close()
    dict = json.loads(jsonString)
    for k in dict:
        global uuidName
        global outFile
        uuidName = dict[k]
        outFile = uuidName + ".mkv"

    ApiServerRequest(uuidName, outFile)


def ApiServerRequest(uuidName, outFile):
    # RequestJobID
    requestJobID_url = "http://163.18.2.36:8887/v2/Session/RequestJobID"
    requestJobID_headers = {'Content-Type': 'application/json'}
    requestJobID_post = requests.post(requestJobID_url, headers=requestJobID_headers)
    requestJobID = requestJobID_post.text
    print("requestJobID:", requestJobID)
    checkAndUpload(uuidName, outFile, requestJobID)


def checkAndUpload(uuidName, outFile, requestJobID):
    # UploadsFiles
    uploadsFiles_url = "http://163.18.2.36:8887/v2/Session/UploadFiles"
    files = os.path.join('.', 'static', 'uploads', outFile)
    sessionID = uuidName
    jobID_jsonData = json.loads(requestJobID, encoding='utf-8')
    jobID = jobID_jsonData['JobID']
    dataSize = os.path.getsize(files)
    uploadsFiles_headers = {"SessionID": sessionID,
                            "JobID": str(jobID),
                            "DataSize": str(dataSize)}
    uploadFiles_server = {"File": open(files, 'rb')}
    uploadFiles_post = requests.post(uploadsFiles_url, headers=uploadsFiles_headers, files=uploadFiles_server)
    uploadFiles = uploadFiles_post.text
    print('uploadFiles:', uploadFiles)
    # print("sessionID_type:", type(sessionID))
    print("sessionID:", sessionID)
    # print("jobID_type:", type(jobID))
    print("jobID:", jobID)
    # print("dataSize_type:", type(dataSize))
    print("dataSize:", dataSize)

    # CheckFiles
    checkFiles_url = "http://163.18.2.36:8887/v2/Session/CheckFiles"
    checkFiles_headers = {'Content-Type': 'application/json'}
    checkFiles_requestBody = {"JobID": str(jobID)}
    checkFiles_post = requests.post(checkFiles_url, headers=checkFiles_headers, data=json.dumps(checkFiles_requestBody))
    checkFiles = checkFiles_post.text
    # print('checkFiles_type:', type(checkFiles))
    print('checkFiles:', checkFiles)
    if checkFiles == '{"Result": false}':
        print('Have missed the packet')
        checkAndUpload(uuidName, outFile, requestJobID)

    # 重新讀取json檔案寫進變數
    jsonFile = open("fileNotUploaded.json", 'r')
    jsonString = jsonFile.read()
    jsonFile.close()

    # 將已經成功上傳的從json檔案中刪除
    dict = json.loads(jsonString)
    print('dict:', dict)
    print('uuidName:', uuidName)
    del dict[uuidName]

    # 將更新後的資料從新寫入json檔案
    jsonFile = open("fileNotUploaded.json", 'w+')
    jsonString = jsonFile.read()
    jsonFile.write(json.dumps(dict))
    jsonFile.close()

    # 更新jsonString變數
    jsonFile = open("fileNotUploaded.json", 'r')
    jsonString = jsonFile.read()
    jsonFile.close()

    if jsonString != "{}":
        ckConnectionAndFile()

if __name__ == "__main__":
    ckConnectionAndFile()
