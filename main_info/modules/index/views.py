# 问句天几高，心中志比天更高
from flask import current_app
from flask import render_template
from flask import session

from main_info import redis_store
from main_info.models import User
from . import index_blue


@index_blue.route('/',methods=['GET','POST'])
def index():
    # 获取用户id
    user_id = session.get('user_id')

    # 查询用户对象
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
    # 返回数据到模板页面(把对象转换为字典)
    data = {
        # 固定语法 如果user为空返回None  如果有返回左边 定义时使用
        "user_info":user.to_dict()if user else None
    }
    # 注意点: 标记了templates为templates_folder之后会自动进入查找
    return render_template('news/index.html',data=data)

@index_blue.route('/favicon.ico')
def favicon_ico():
    return current_app.send_static_file('news/favicon.ico')