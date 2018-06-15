# 问句天几高，心中志比天更高
from flask import current_app
from flask import g
from flask import render_template
from flask import session

from main_info.models import User
from main_info.utils.common import user_login_data
from . import news_blue


#获取新闻详情信息
# 请求路径: /news/<int:news_id>
# 请求方式: GET
# 请求参数:news_id
# 返回值: detail.html页面, 用户data字典数据
@news_blue.route('/<int:news_id>')
@user_login_data
def news_detail(news_id):
    # 拼接数据
    data = {
        "user_info":g.user.to_dict() if g.user else None
    }
    return render_template('news/detail.html',data=data)