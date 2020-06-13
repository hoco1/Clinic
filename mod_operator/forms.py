from flask_wtf import FlaskForm
from wtforms import PasswordField,TextField,TextAreaField
from utils.forms import MultipleCheckboxField
from wtforms.validators import DataRequired

class LoginOperator(FlaskForm):
    personnelname = TextField('personnelname',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])

class PersonnelForm(FlaskForm):
    personnelname=TextField('personnelname',validators=[DataRequired()])
    madraktype=TextField('madraktype')
    phone=TextField('phone',validators=[DataRequired()])
    mobile=TextField('mobile')
    mellicode=TextField('mellicode',validators=[DataRequired()])
    address=TextAreaField('address')
    password=PasswordField('password',validators=[DataRequired()])
    confirm_pass=PasswordField('confirm_pass',validators=[DataRequired()])
    role = MultipleCheckboxField(coerce=int)
    sicks=MultipleCheckboxField(coerce=int)

class SickForm(FlaskForm):
    bimarname=TextField('bimarname',validators=[DataRequired()])
    bimehcode=TextField('bimehcode',validators=[DataRequired()])
    telph=TextField('telph',validators=[DataRequired()])
    mobile=TextField('mobile',validators=[DataRequired()])
    mellicode=TextField('mellicode',validators=[DataRequired()])
    address=TextAreaField('address',validators=[DataRequired()])
    notes=TextAreaField('notes') 
    bimetype=MultipleCheckboxField(coerce=int)
    haghalzahmeh=MultipleCheckboxField(coerce=int)
    personnels = MultipleCheckboxField(coerce=int)

class SearchForm(FlaskForm):
    search_query = TextField(validators=[DataRequired()])


