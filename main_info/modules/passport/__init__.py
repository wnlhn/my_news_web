# 问句天几高，心中志比天更高
from flask import Blueprint
# 创建蓝图对象,并且设置访问前缀
passprot_blue = Blueprint('passport_blue',__name__,url_prefix='/passport')

from . import views
