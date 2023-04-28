cd %~dp0
IF NOT exist venv (python -m venv venv\)
venv\Scripts\python.exe venv\Lib\site-packages\pip\__main__.py install -r requirements.txt
PAUSE