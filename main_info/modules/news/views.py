# 问句天几高，心中志比天更高
from flask import abort
from flask import current_app, jsonify
from flask import g
from flask import render_template
from flask import request
from flask import session

from main_info import constants, db
from main_info.models import News, Comment
from main_info.response_code import RET
from main_info.utils.common import user_login_data
from . import news_blue


# 新闻评论的实现
# 请求路径: /news/news_comment
# 请求方式: POST
# 请求参数:news_id,comment,parent_id, g.user
# 返回值: errno,errmsg,评论字典
@news_blue.route('/news_comment',methods=['POST'])
@user_login_data
def comment():
    # 判断是否登陆
    if not g.user:
        return jsonify(errno=RET.DATAERR,errmsg='用户未登陆')
    # 获取数据
    data_dict = request.json
    news_id = data_dict.get('news_id')
    content = data_dict.get('comment')
    parent_id = data_dict.get('parent_id')

    # 校验数据
    if not all([news_id,content,g.user]):
        return jsonify(errno=RET.PARAMERR,errmsg='参数错误')

    # 相应操作
    comment = Comment()
    comment.user_id = g.user.id
    comment.news_id = news_id
    comment.content = content
    if parent_id:
        comment.parent_id = parent_id
    # 提交到数据库
    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='评论失败')
    # 返回前端
    return  jsonify(errno=RET.OK,errmsg='操作成功',data=comment.to_dict())







# 实现收藏/取消收藏
# 请求路径: /news/news_collect
# 请求方式: POST
# 请求参数:news_id,action, g.user
# 返回值: errno,errmsg

@news_blue.route('/news_collect',methods=['POST'])
@user_login_data
def news_collecte():
    # 判断用户是否登陆
    if not g.user:
        return jsonify(errno=RET.NODATA,errmsg='用户未登录')
    # 获取数据
    dict = request.json
    news_id = dict.get('news_id')
    action = dict.get('action')

    # 校验数据
    if not all([news_id,action,g.user]):
        return jsonify(errno=RET.PARAMERR,errmsg='参数错误')

    if not action in ['collect','cancel_collect']:
        return jsonify(errno=RET.DATAERR,errmsg='操作类型错误')
    # 取出新闻对象方便下面的操作
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
    if not news:
        return jsonify(errno=RET.DBERR,errmsg='该新闻不存在')
    #根据操作类型进行相应的操作
    if action == 'collect':
        g.user.collection_news.append(news)
    else:
        g.user.collection_news.remove(news)

    # 返回前段
    return jsonify(errno=RET.OK,errmsg='操作成功')











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
    # 新闻对象列表转为字典列表,返回前端使用
    news_to_list = []
    for news in news_list:
        news_to_list.append(news.to_dict())


    # 显示正文内容实现
    # 通过news_id查询news对象
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='数据库查询失败')
    if not news:
        # 如果找不到就显示404错误，以后会对404页面进行特殊处理
        abort(404)

    # 收藏列表显示　后端实现
    # 判断用户是否已经收藏此新闻，默认是False
    is_collected = False
    if g.user and news in g.user.collection_news:
        is_collected = True

    # 取出所有的评论对象,并转化为字典列表
    try:
        contents = Comment.query.filter(Comment.news_id  == news.id).order_by(Comment.create_time.desc()).all()
    except Exception as e:
        current_app.logger.error(e)

    comments = []
    for comment in contents:
        comments.append(comment.to_dict())


    data = {
        "user_info": g.user.to_dict() if g.user else None,
        "user_news_list": user_news_list,
        "user_fans": user_fans,
        "news_list":news_to_list,
        "news_info":news.to_dict(), # 将对象转化为列表方便前端使用
        "is_collected":is_collected,
        "comments":comments
    }
    return render_template('news/detail.html',data=data)





















