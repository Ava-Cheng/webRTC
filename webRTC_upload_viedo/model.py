from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

#  取得目前文件資料夾路徑
pjdir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
#  新版本的部份預設為none，會有異常，再設置True即可。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#  設置sqlite檔案路徑
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(pjdir, 'webrtc.sqlite')

db = SQLAlchemy(app)
class Webrtc(db.Model):
    __tablename__ = 'Webrtc_upload'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Webrtc %r>' % self.name