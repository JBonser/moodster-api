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
flask db init && flask db migrate && flask db upgrade -x data=true
```
To run the application in development first set the flask app env var:
```
export FLASK_APP=app.__main__
```
Then simply call:
```
flask run
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

# Instigating Database Migrations
If you change the database models by either:
* Adding/Removing Tables
* Adding/Removing Fields from a table

Then you will need to trigger a migration like so:
First check you are at the latest version.
```
flask db current
```
If the hash does not match the latest version file in the migrations folder then you need to run an upgrade to get to the head.
```
flask db upgrade head -x data=true
```
Then you can tell flask migrate to run.
```
flask db migrate
```
This will look at your database models and attempt to find out what exactly has changed.
You should ensure you go through the resulting version file and check that what has been generated makes sense.

Finally upgrade to this new database version by running an upgrade again
```
flask db upgrade head -x data=true
```