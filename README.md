# Moodster-API
Moodster API Project

# Setting up the Development Environment
```
python3 -m venv env
source env/bin/activate
pip install -e .
```


# Running the Application
## Development
If running for the first time you will need to create the DB, run:
```
flask db init && flask db migrate && flask db upgrade
```
To run the application in development simply call:
```
export FLASK_APP=app.__main__; flask run;
```
alternatively you can simply run the app package:
```
python app/
```


# Running the Tests
To run the unit tests use the unittest discovery like so:
```
python -m unittest discover app/tests/
```
