# 问句天几高，心中志比天更高
# 自定义模板过滤器
from functools import wraps

from flask import current_app
from flask import g
from flask import session


def do_index_filter(index):
    if index == 1:
        return 'first'
    elif index == 2:
        return 'second'
    elif index == 3:
        return 'third'
    else:
        return ''


# 装饰器封装用户登陆数据
def user_login_data(func):
    @wraps(func)
    def user_inner(*args,**kwargs):
        # 获取用户编号
        user_id = session.get('user_id')
        # 查询用户对象
        user = None
        if user_id:
            try:
                from main_info.models import User
                user = User.query.get(user_id)
            except Exception as e:
                current_app.logger.error(e)

        # 使用g对象保存user对象
        g.user = user
        return func(*args,**kwargs)
    return user_inner
