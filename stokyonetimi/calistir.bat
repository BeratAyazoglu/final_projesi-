@echo off

echo Flask uygulamanızı başlatıyoruz...
start python app.py
timeout /t 1
start http://127.0.0.1:5000
