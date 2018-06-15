# 问句天几高，心中志比天更高
from flask import current_app, jsonify
from flask import g
from flask import render_template
from flask import session

from main_info import constants
from main_info.models import User, News
from main_info.response_code import RET
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
    if g.user:
        user_news_list = g.user.news_list
        user_fans = g.user.followers
    else:
        user_news_list = ""
        user_fans = ""

    # 显示热门新闻排行榜
    # 查询出数据库点击数量最多的１０条新闻
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='数据库查询失败')
    data = {
        "user_info": g.user.to_dict() if g.user else None,
        "user_news_list": user_news_list,
        "user_fans": user_fans,
        "news_list":news_list
    }
    return render_template('news/detail.html',data=data)