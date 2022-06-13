# Web app Agile :calendar:
Web app for project management that using agile Scrum methodology

### How to run

1. Enable virtual enviroment with `<venv>/Scripts/activate`
2. Set debug mode with `$env:FLASK_ENV = "development"` (on PowerShell) `set FLASK_ENV=development` (on CMD)
3. Run with `flask run`

### Update db structure

1. Open a python shell inside the project folder
2. Import the update function with `from backend.database import init_db`
3. Run the update function with `init_db()`

Made by:

- [Paolo Zanotti](https://github.com/zanottipaolo)
- [Federico De Duro](https://github.com/Jfkmdd)
- [Matteo Soldini](https://github.com/matteosoldini)
