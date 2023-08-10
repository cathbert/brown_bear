@echo off

python -m virtualenv .venv

python -m pip install -r requirements.txt

.venv\Scripts\python.exe main.py

pause