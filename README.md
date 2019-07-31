# webRTC_upload_viedo
## 本次需要執行之步驟：
### model.py
- 資料庫初始化設定
- Id=>Integer.   primary_key
- name=> String(40).   unique=True

### app_offline_upload_sqlite.py
- 錄影
- 存檔.webm格式
- 轉檔.mkv H.264格式
- 將檔名寫入DB


### app_offline_transfer_sqlite.py

- 測試連線及資料庫是否有資料
兩者皆成立則執行接下來步驟，其一不成立則重複執行
- 從DB存取檔案名稱
- 上傳作業
- 請求jobID
- 上傳檔案（sessionID、jobID、dataSize）post過去
- 確認上傳完整性（無完整則重新執行上傳檔案步驟）
- 刪除已成功上傳檔名
- 重新執行


- 架構
![](https://d2mxuefqeaa7sj.cloudfront.net/s_009CECF180D456AA56C8822DB0DE14B8C97842F05B48B7F0C7B7C8302CC5503F_1551932328357_+2019-03-07+12.18.18.png)

### 執行方式：
- 即時版：python3.6 app_immediate.py
- URL:https://127.0.0.1:8880/audiovideo
- 離線版(用json檔案紀錄)：python3.6 app_offline_transfer.py(轉檔)
- python3.6 app_offline_upload.py (上傳)  
- URL:https://127.0.0.1:8881/audiovideo
- 未上傳檔案紀錄：fileNotUploaded.json
- 離線版(用DB紀錄)：python3.6 app_offline_transfer_sqlite.py(轉檔)
- python3.6 app_offline_upload_sqlite.py (上傳)
- URL:https://127.0.0.1:8882/audiovideo
- 未上傳檔案紀錄：webrtc.sqlite

### 檔案存放位置(.mkv/.webm):webRTC_upload_viedo/static/uploads
