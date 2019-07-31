# -*- coding: UTF-8 -*-
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import uuid
import os
import subprocess
import requests
import json

app = Flask(__name__)


@app.route('/audiovideo')
def upload_file():
   return render_template('index.html')


@app.route('/audiovideo', methods=['GET', 'POST'])
def audiovideo():
    if request.method == 'POST':
        # 將影像存成.mkv
        file = request.files['audiovideo']
        uuidName = str(uuid.uuid1())
        filename_mkv = uuidName + ".mkv"
        filename = secure_filename(filename_mkv)
        file_save_path = os.path.join('.', 'static', 'uploads', filename_mkv)
        file.save(file_save_path)

        # 轉檔 webm->mkv H.264
        '''
        outfile = uuidName + ".mkv"
        upload_path_mkv = os.path.join('.', 'static', 'uploads', outfile)
        subprocess.call(['ffmpeg', '-i', file_save_path, upload_path_mkv])
        '''
        ApiServerRequest(uuidName, filename_mkv)
    return "susses"


def ApiServerRequest(uuidName, outfile):
    # RequestJobID
    requestJobID_url = "http://163.18.2.36:8887/v2/Session/RequestJobID"
    requestJobID_headers = {'Content-Type': 'application/json'}
    requestJobID_post = requests.post(requestJobID_url, headers=requestJobID_headers)
    requestJobID = requestJobID_post.text
    print("requestJobID:", requestJobID)
    checkAndUpload(uuidName, outfile, requestJobID)


def checkAndUpload(uuidName, outfile, requestJobID):
    # UploadsFiles
    uploadsFiles_url = "http://163.18.2.36:8887/v2/Session/UploadFiles"
    files = os.path.join('.', 'static', 'uploads', outfile)
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
        checkAndUpload(uuidName, outfile, requestJobID)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8880, ssl_context=(
        "./rtc-video-room-cert.pem",
        "./rtc-video-room-key.pem"
    ))

