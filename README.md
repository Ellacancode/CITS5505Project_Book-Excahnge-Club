# CITS5505 Project: Book Club

## how to run unit tests on a Mac Computer

Please follow the exact command 

1.source Book_env/Scripts/activate

2.export FLASK_APP=Bookclub 

3.export FLASK_ENV=testing  (This is to enter the test environment i configured earlier)

4.python -m unittest discover -s test -p "test_*.py" -v (run all tests)

5.coverage run -m unittest discover -s test -p "test_*.py" -v (run all tests to check test coverage,this is optional)

6.coverage report (generate coverage report in terminal)

7.coverage HTML (get detailed coverage report)

## how to run selenium test on a Mac Computer

1.install selenium:

pip install selenium

2. Download webDriver match your Chome Browser version, and extract and place the Chromedriver executable in the test directory.

3. To run the test, please make sure the server is running

4. In a new terminal:
   python tests_selenium.py





## Project Overview
This document provides setup and migration instructions for the Book Club project, a Flask-based web application. 
## Setup Instructions

### Step 1: Create a Virtual Environment
These instructions are tailored for a Windows environment.

To isolate our project dependencies, we start by creating a virtual environment:
```bash
python -m venv Book_Env
```

### Step 2: Install Required Packages
Install all dependencies listed in the requirements.txt file:
```bash
pip install -r requirements.txt
```

### Step 3: Activate the Virtual Environment
To activate the virtual environment and use it for running the application, execute:

For Windows
```bash
.\Book_Env\Scripts\activate
```
For Mac
```bash
source Book_Env/bin/activate
```


### Step 4: Set Environment Variables
Set the necessary Flask environment variables and debug model for running your application:

For Windows:
```bash
$env:FLASK_APP = "Bookclub"
$env:FLASK_DEBUG = "1"
```

For Mac:
```bash
export FLASK_APP=Bookclub
export FLASK_DEBUG=1
```

### Step 5: Run the Flask Application
To start the Flask application, use the following command:

```bash
flask run
```

## Database Migration
### Step 1: Initialize the Database
Before running the application, you must initialize the database with:
```bash
flask db init
```

### Step 2: Generate and Apply the New Migration to the Database
Generate a new migration file if there are changes to the database models and update the database schema, apply the generated migration:
```bash
flask --app Bookclub db migrate -m "message of migration"
flask db upgrade
```


## Project Members

| UWA ID    | Name         | GitHub Username |
|-----------|------------  |-----------------|
| 23829101  | Long Qin     | LongQin0121     |
| 23844446  | Ella Zhang   | Ellacancode     |
| 23825634  | Yunwei Zhang | Yunwei-Zhang    |
| 21978612  | Lucy Chen    | lucychen0305    |
|           |              |                 |
