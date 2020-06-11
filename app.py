from flask import Flask

app = Flask(__name__)

import views

from mod_doctor import doctor 
from mod_operator import operator 
from mod_sick import sick 
from mod_upload import uploads

app.register_blueprint(doctor)
app.register_blueprint(operator)
app.register_blueprint(sick)
app.register_blueprint(uploads)