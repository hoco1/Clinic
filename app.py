from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Development
app = Flask(__name__)
app.config.from_object(Development)
db = SQLAlchemy(app)
migrate = Migrate(app,db)

from views import *

from mod_doctor import doctor 
from mod_operator import operator
from mod_nurse import nurse 
from mod_upload import uploads

app.register_blueprint(doctor)
app.register_blueprint(operator)
app.register_blueprint(nurse)
app.register_blueprint(uploads)