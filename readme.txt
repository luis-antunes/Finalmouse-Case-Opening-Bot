Code to create binary:
pyinstaller --onefile --icon=bot.ico --add-data "venv\Lib\site-packages\pyfiglet;./pyfiglet" CaseOpeningBot.py