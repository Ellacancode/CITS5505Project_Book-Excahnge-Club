# CITS5505 Project: Book Club
This document provides purpose,setup and migration instructions for the Book Club project, a Flask-based web application. 


## Project Purpose

The UWA Book Club website is designed to effectively engage students in sharing their ideas about books, reading books, and borrowing books. Our mission is to build a community at UWA through a shared love of books.

**Purpose**
By registering and logging into our website, students can:

Participate in Discussions: Join discussions in the forum by posting or commenting. Use the forum search to explore other users' interactions.<br>
Interact with Peers: Follow other users and like their posts to engage with the community.<br>
Discover Books: Find books via the bookshelf page by browsing or searching by title, genre, author, or status.<br>
Personalize Profiles: Customize their profiles by updating their "About Me" section and profile picture.<br>

**Admin Functions**
Our website includes special features for administrators，you can login using admin@admin.com and password Admin@12

Moderation: Admins have special accounts to log in and monitor posts, comments, and books. If any content contains inappropriate language or behavior, admins can delete posts, users, comments, or likes.
We designed the UWA Book Club website with love and hope it brings value to our community. 

## Let's start your reading journey together. Simply register and join us today!



## Project Members

| UWA ID    | Name         | GitHub Username |
|-----------|------------  |-----------------|
| 23829101  | Long Qin     | LongQin0121     |
| 23844446  | Ella Zhang   | Ellacancode     |
| 23825634  | Yunwei Zhang | Yunwei-Zhang    |
| 21978612  | Lucy Chen    | lucychen0305    |
|           |              |                 |


## The architecture of the web application
**Model View Controller**
<br>
<div align=center><img src="https://www.mathworks.com/company/newsletters/articles/developing-matlab-apps-using-the-model-view-controller-pattern/_jcr_content/mainParsys/image.adapt.full.medium.jpg/1668175030977.jpg"[1] width="420" height="280" alt="MVC"/>
</div>
<br>
MVC is widely attributed to Trygve Reenskaug, who reportedly invented it in the 1970s. Since then, it has gained immense popularity as a dominant pattern for server-side web applications[2].
In this project, we have 6 tables with 6 relationships.
<br>

**Model - Tables:**
<br>
**User:** Represents users of the application.<br>
**Post:** Represents blog posts created by users.<br>
**Comment:** Represents comments made on blog posts.<br>
**Like:** Represents likes given to blog posts by users.<br>
**Book:** Represents books in the database.<br>
**Followers:** A many-to-many relationship table to manage user followers.<br>

**Model - Relationships:**
#### <span style="color: green;">User-Post</span>: One-to-many relationship. Each user can have multiple posts.
#### <span style="color: green;">User-Comment</span>: One-to-many relationship. Each user can have multiple comments.
#### <span style="color: green;">User-Like</span>: One-to-many relationship. Each user can have multiple likes.
#### <span style="color: green;">Post-Comment</span>: One-to-many relationship. Each post can have multiple comments.
#### <span style="color: green;">Post-Like</span>: One-to-many relationship. Each post can have multiple likes.
#### <span style="color: green;">User-Followers</span>: Many-to-many relationship managed by the followers table. Users can follow and be followed by multiple users.
<br>

**Controller**

The controller acts as an intermediary between the models and views. It facilitates the transfer of data between the browser and the app, as well as vice versa. In this project, the "routes.py" file functions as the controller. <br> Controller

The Controller handles user requests, processes data via models (User, Post, Book, Comment, Like), and renders templates. It manages routes for registration, login, posting, commenting, and searching books.

**View**

The view is the component of the app through which users directly interact.  The HTML files within the "template" folder serve as the views. Users can access information, read it, and interact with it[3].


![Home Page](Bookclub/static/readme/1.png)

![User Profile](Bookclub/static/readme/2.png)

![Forum Page](Bookclub/static/readme/3.jpg)

## How to launch the project

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
## How to run unit tests 
Enter the test environment 
### For Mac:
```bash
export FLASK_ENV=testing  
```
### For Window:
```bash
$env:FLASK_APP = testing"
```

### Run the tests:
```bash
python -m unittest discover -s test -p "test_*.py" -v 
```
Run all tests to check test coverage,this is optional
```bash
coverage run -m unittest discover -s test -p "test_*.py" -v 
```
Generate coverage report in terminal
```bash
coverage report 
```
Get detailed coverage report
```bash
coverage HTML 
```

## How to run selenium test 

1.install selenium:
   ```bash
      pip install selenium
   ```  
2. Download webDriver match the Chome Browser version, and extract and place the Chromedriver executable in the test directory.
3. To run the test, please make sure the server is running
4. In a new terminal:
   ```bash
      python test/tests_selenium.py
   ```      


## References

[1] https://www.mathworks.com/company/newsletters/articles/developing-matlab-apps-using-the-model-view-controller-pattern.html

[2] Reenskaug, T. (1979). Models-Views-Controllers. Retrieved from http://heim.ifi.uio.no/~trygver/themes/mvc/mvc-index.html

[3] http://heim.ifi.uio.no/~trygver/themes/mvc/mvc-index.html
 
[4] [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) by **Miguel Grinberg**.

[5] Insights and assistance provided by ChatGPT, a language model by OpenAI.
