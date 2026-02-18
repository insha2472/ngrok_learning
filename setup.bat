@echo off
call venv\Scripts\activate
pip install psycopg2-binary python-dotenv
python create_tables.py
pause
