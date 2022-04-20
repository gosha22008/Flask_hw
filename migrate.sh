export FLASK_APP=my_app.py
flask db init
flask db migrate
flask db upgrade