# 问句天几高，心中志比天更高
from flask import current_app
from flask import render_template
from flask import session

from main_info.models import User
from . import news_blue


#获取新闻详情信息
# 请求路径: /news/<int:news_id>
# 请求方式: GET
# 请求参数:news_id
# 返回值: detail.html页面, 用户data字典数据
@news_blue.route('/<int:news_id>')
def news_detail(news_id):
    # 获取用户编号
    user_id = session.get('user_id')
    # 通过编号获取用户对象
    user = None
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)

    # 拼接数据
    data = {
        "user_info":user.to_dict() if user else None
    }
    return render_template('news/detail.html',data=data)