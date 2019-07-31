# -*- coding: UTF-8 -*-
from model import db
from model import Webrtc
import os
import requests
import json
import time
import socket
import subprocess


def ckConnectionAndFile():
    # 查看目前DB內data數量
    allUUIDName = Webrtc.query.all()
    dataNum = len(allUUIDName)
    print('dataNum:', dataNum)

    if dataNum == 0:
        t = time.time()
        while True:
            if time.time()-t > 10:
                ckConnectionAndFile()
            time.sleep(10)

    # 判斷DB是否有資料及是否有連線
    url = "www.google.com"
    try:
        host = socket.gethostbyname(url)
        s = socket.create_connection((host, 80), 2)
        dbData()
    except Exception as e:
        t = time.time()
        while True:
            if time.time()-t > 10:
                print('No connection')
                ckConnectionAndFile()
            time.sleep(10)


def dbData():
    # 從DB取得檔名
    allUUIDName = Webrtc.query.all()
    uuidName = allUUIDName[0].name
    outFile = uuidName + ".mkv"

    apiServerRequest(uuidName, outFile)


def apiServerRequest(uuidName, outFile):
    # RequestJobID
    requestJobID_url = "http://163.18.2.36:8887/v2/Session/RequestJobID"
    requestJobID_headers = {'Content-Type': 'application/json'}
    requestJobID_post = requests.post(requestJobID_url, headers=requestJobID_headers)
    requestJobID = requestJobID_post.text
    print("requestJobID:", requestJobID)

    uploadFileAndCheck(uuidName, outFile, requestJobID)


def uploadFileAndCheck(uuidName, outFile, requestJobID):
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
        uploadFile(uuidName, outFile, requestJobID)

    updateDB(uuidName)


def updateDB(uuidName):
    # 將已經上傳的檔案名稱從資料庫中刪除
    query_webrtc = Ｗebrtc.query.filter_by(name=uuidName).first()
    db.session.delete(query_webrtc)
    db.session.commit()

    # 顯示目前資料庫剩餘檔案名稱
    allUUIDName = Webrtc.query.all()
    print("db_webrtc_upload:", allUUIDName)

    ckConnectionAndFile()


if __name__ == "__main__":
    ckConnectionAndFile()
