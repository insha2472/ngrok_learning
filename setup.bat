@echo off
call venv\Scripts\activate
pip install -r requirements.txt
python create_tables.py
pause
