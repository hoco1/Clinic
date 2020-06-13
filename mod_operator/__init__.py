from flask import Blueprint

operator = Blueprint('operator',__name__,url_prefix='/operator')

from .views import *
from .models import *
