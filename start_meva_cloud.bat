@echo off
cd /d C:\works\MEVA_Cloud
C:\works\python\.venv-mink-main\Scripts\python.exe -m uvicorn server.main:app --host 127.0.0.1 --port 8000 --reload
