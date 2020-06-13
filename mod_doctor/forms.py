from flask_wtf import FlaskForm
from wtforms import TextField,TextAreaField,PasswordField
from wtforms.validators import DataRequired
from utils.forms import MultipleCheckboxField

class LoginDoctor(FlaskForm):
    personnelname = TextField('personnelname',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])

class SickDoctorForm(FlaskForm):
    bimaritype=TextAreaField('bimaritype',validators=[DataRequired()])
    notes=TextAreaField('notes') 
    
class SearchForm(FlaskForm):
    search_query = TextField(validators=[DataRequired()])

