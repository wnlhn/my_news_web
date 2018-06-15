# 问句天几高，心中志比天更高
from flask import current_app, jsonify
from flask import g
from flask import render_template
from flask import request
from flask import session

from main_info import constants
from main_info import redis_store
from main_info.models import User, News, Category
from main_info.response_code import RET
from main_info.utils.common import user_login_data
from . import index_blue

#首页新闻列表
# 请求路径: /newslist
# 请求方式: GET
# 请求参数: cid,page,per_page
# 返回值: data数据
@index_blue.route('/newslist',methods=['GET'])
def newslist():
    """
      思路分析
      1.获取参数
      2.校验参数,转换参数类型
      3.根据条件查询数据
      4.将查询到的分类对象数据,转成字典
      5.返回响应请求
      :return:
    """
    # 1.获取参数
    cid = request.args.get('cid')
    page = request.args.get('page',1)
    per_page = request.args.get('per_page',10)

    # 2.校验参数, 转换参数类型
    try:
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1
        per_page = 10

    # 3.根据条件查询数据
    try:
        list = []
        if cid != '1':
            list.append(News.category_id == cid)
        paginate = News.query.filter(*list).order_by(News.create_time.desc()).paginate(page,per_page,False)
        # 获取分页中的内容,总页数,当前页,当前页的所有对象
        totalPage = paginate.pages
        currentPage = paginate.page
        items = paginate.items
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error=RET.DBERR,errmsg='查询数据失败')

    # 4.将查询到的分类对象数据, 转成字典
    newsList = []
    for news in items:
        newsList.append(news.to_dict())
    # 5.返回响应请求
    return jsonify(error= RET.OK,errmsg='获取成功',cid=cid,currentPage=currentPage,totalPage=totalPage,newsList=newsList)



@index_blue.route('/',methods=['GET','POST'])
@user_login_data
def index():

    # 查询数据库,按照点击量查询前十条新闻
    try:
        new_list = News.query.order_by(News.clicks.desc()).limit(constants.HOME_PAGE_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    # 把对象列表转换为字典列表
    news_list_dic = []
    for new in new_list:
        news_list_dic.append(new.to_dict())

    # 查询数据库的分类信息
    try:
        categoies = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)
    # 把对象列表转化为字典列表
    cate_list = []
    for cate in categoies:
        cate_list.append(cate.to_dict())

    # 返回数据到模板页面(把对象转换为字典)
    data = {
        # 固定语法 如果user为空返回None  如果有返回左边 定义时使用
        "user_info":g.user.to_dict()if g.user else None,
        "news_list":news_list_dic,
        "cate_list":cate_list
    }
    # 注意点: 标记了templates为templates_folder之后会自动进入查找
    print(data['cate_list'])
    return render_template('news/index.html',data=data)

@index_blue.route('/favicon.ico')
def favicon_ico():
    return current_app.send_static_file('news/favicon.ico')