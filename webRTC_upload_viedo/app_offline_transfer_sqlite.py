# -*- coding: UTF-8 -*-
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from model import db
from model import Webrtc
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
        print(request.data)
        print(request.files)
        file = request.files['audiovideo']
        uuidName = str(uuid.uuid1())
        filename_webm = uuidName + ".mkv"
        filename = secure_filename(filename_webm)
        file_save_path = os.path.join('.', 'static', 'uploads', filename_webm)
        file.save(file_save_path)

        # 轉檔 webm->mkv H.264
        '''
        outFile = uuidName + ".mkv"
        upload_path_mkv = os.path.join('.', 'static', 'uploads', outFile)
        subprocess.call(['ffmpeg', '-i', file_save_path, upload_path_mkv])
        '''

        # 寫入
        names = Webrtc(uuidName)
        db.session.add(names)
        db.session.commit()

    return "susses"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8882, ssl_context=(
        "./rtc-video-room-cert.pem",
        "./rtc-video-room-key.pem"
    ))
