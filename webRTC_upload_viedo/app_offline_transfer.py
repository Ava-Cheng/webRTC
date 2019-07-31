# -*- coding: UTF-8 -*-
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import uuid
import os
import subprocess
import json


app = Flask(__name__)


@app.route('/audiovideo')
def upload_file():
   return render_template('index.html')


@app.route('/audiovideo', methods=['GET', 'POST'])
def audiovideo():
    if request.method == 'POST':
        # 將影像存成.webm
        file = request.files['audiovideo']
        uuidName = str(uuid.uuid1())
        filename_webm = uuidName + ".webm"
        filename = secure_filename(filename_webm)
        file_save_path = os.path.join('.', 'static', 'uploads', filename_webm)
        file.save(file_save_path)

        # 轉檔 webm->mkv H.264
        outFile = uuidName + ".mkv"
        upload_path_mkv = os.path.join('.', 'static', 'uploads', outFile)
        subprocess.call(['ffmpeg', '-i', file_save_path, upload_path_mkv])

        # 未上傳檔案紀錄，如果不存在則檔案建立
        fileNotUploaded = os.path.join('.', 'fileNotUploaded.json')
        if not os.path.isfile(fileNotUploaded):
            jsonFile = open('fileNotUploaded.json', 'w+')
            jsonFile.write('{ }')
            jsonFile.close()

        # 不管有沒有連線先將uuid寫入檔案做紀錄
        jsonFile = open("fileNotUploaded.json", 'r')
        jsonString = jsonFile.read()
        jsonFile.close()
        dict = json.loads(jsonString)
        jsonFile = open("fileNotUploaded.json", 'w+')
        dict[uuidName] = uuidName
        jsonFile.write(json.dumps(dict))
        jsonFile.close()
    return "susses"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8881, ssl_context=(
        "./rtc-video-room-cert.pem",
        "./rtc-video-room-key.pem"
    ))

