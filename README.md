#  CITS5505Project_Book-Excahnge-Club


###  !!! For Window !!!
.\Book_Env\Scripts\activate

$env:FLASK_APP = "Bookclub"    

$env:FLASK_DEBUG = "1"

flask run
###



###  Migration
flask --app Bookclub db migrate -m "message"

flask db upgrade
###