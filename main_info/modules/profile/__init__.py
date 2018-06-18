# 问句天几高，心中志比天更高
from flask import Blueprint


profile_blue = Blueprint('profile_blue',__name__,url_prefix='/profile')

from . import views