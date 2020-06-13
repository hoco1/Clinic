from flask_wtf import FlaskForm
from wtforms import TextField,TextAreaField,PasswordField
from wtforms.validators import DataRequired
from utils.forms import MultipleCheckboxField

class SearchForm(FlaskForm):
    search_query = TextField(validators=[DataRequired()])

class ResNoskhe(FlaskForm):
    result = MultipleCheckboxField(coerce=int)
    

class LoginNurse(FlaskForm):
    personnelname = TextField('personnelname',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])