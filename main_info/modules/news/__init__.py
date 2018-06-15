# 问句天几高，心中志比天更高
from flask import Blueprint

news_blue = Blueprint('news_blue',__name__,url_prefix='/news')

from . import views