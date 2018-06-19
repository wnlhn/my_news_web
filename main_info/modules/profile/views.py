# 问句天几高，心中志比天更高
from flask import current_app
from flask import g, jsonify
from flask import redirect
from flask import render_template
from flask import request
from main_info.models import Category,News


from main_info import constants,db
from main_info.response_code import RET
from main_info.utils.common import user_login_data
from . import profile_blue

# 上传头像
# 请求路径: /user/pic_info
# 请求方式:GET,POST
# 请求参数:无, POST有参数,avatar
# 返回值:GET请求: user_pci_info.html页面,data字典数据, POST请求: errno, errmsg,avatar_url
@profile_blue.route('/pic_info')
@user_login_data
def pic_info():
    data = {
        "user_info":g.user.to_dict()
    }
    return render_template('news/user_pic_info.html',data = data)


# 新闻列表显示
@profile_blue.route('/news_list')
@user_login_data
def news_list():
    # 获取参数p
    page = request.args.get('p',1)
    # 类型转换
    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    # 获取分页对象
    paginate = News.query.filter(News.user_id == g.user.id).paginate(page,3,False)
    # 获取分页数据
    page = paginate.page
    page_totle = paginate.pages
    items = paginate.items

    # 转化成字典供前端使用
    news_dict = []
    for item in items:
        news_dict.append(item.to_dict())
    # 返回前端
    data = {
        "page":page,
        "totle_page":page_totle,
        "news_list":news_dict
    }
    return render_template('news/user_news_list.html',data=data)



# 收藏显示
@profile_blue.route('/collection')
@user_login_data
def collection():
    # 获取参数p
    page = request.args.get('p',1)
    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1
    try:
        paginate = g.user.collection_news.paginate(page,constants.USER_COLLECTION_MAX_NEWS,False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='数据库查询失败')
    # 将分页对象中的数据取出来
    totle_page = paginate.pages
    current_page = paginate.page
    items = paginate.items
    collections = []
    for collection in items:
        collections.append(collection.to_dict())
    data = {
        "total_page":totle_page,
        "current_page": current_page,
        "collections":collections
    }
    return render_template('news/user_collection.html',data=data)

# 新闻发布
@profile_blue.route('/news_release',methods=['POST','GET'])
@user_login_data
def news_release():
    if request.method == 'GET':
        category_list = Category.query.all()
        categories = []
        for category in category_list:
            category_dic = category.to_dict()
            if category_dic['id'] != 1:
                categories.append(category_dic)
        data = {
            'categories':categories
        }
        return render_template('news/user_news_release.html',data=data)
    # 获取参数
    title = request.form.get('title')
    category_id = request.form.get('category_id')
    digest = request.form.get('digest')
    content = request.form.get('content')

    # 校验参数
    if not all([title,category_id,digest,content]):
        return jsonify(errno=RET.PARAMERR,errmsg='参数不完整')

    # 创建新闻对象
    try:
        news_obj = News()
        news_obj.title = title
        news_obj.source = '个人发布'
        news_obj.digest = digest
        news_obj.content = content
        news_obj.category_id = category_id
        news_obj.user_id = g.user.id
        news_obj.status = 1
        db.session.add(news_obj)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='数据库错误')
    # 返回前端
    return jsonify(err=RET.OK,errmsg='操作成功')








# 修改密码
@profile_blue.route('/pass_info',methods=['POST','GET'])
@user_login_data
def pass_info():
    if request.method == 'GET':
        return render_template('news/user_pass_info.html')
    data_dict = request.json
    old_password = data_dict.get('old_password')
    new_password = data_dict.get('new_password')
    if not all([old_password,new_password]):
        return jsonify(errno=RET.PARAMERR,errmsg='参数不完整')
    if not g.user.check_passowrd(old_password):
        return jsonify(errno=RET.PARAMERR,errmsg='原始密码错误')
    try:
        g.user.password = new_password
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='数据库修改失败')
    return jsonify(errno=RET.OK,errmsg='操作成功')





# 显示基本信息
# 请求路径: /user/base_info
# 请求方式:GET,POST
# 请求参数:POST请求有参数,nick_name,signature,gender
# 返回值:errno,errmsg
@profile_blue.route('/base_info',methods=['GET','POST'])
@user_login_data
def base_info():
    if request.method == 'GET':
        data = {
            'user_info':g.user.to_dict()
        }
        return render_template('news/user_base_info.html',data=data)
    # 获取数据
    data_dict = request.json
    nick_name = data_dict.get('nick_name')
    signature = data_dict.get('signature')
    gender = data_dict.get('gender')

    # 校验数据
    if not all([nick_name,signature,gender]):
        return jsonify(errno=RET.PARAMERR,errmsg='参数不完整')

    # 操作数据库
    try:
        g.user.nick_name = nick_name
        g.user.signature = signature
        g.user.gender = gender
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='数据库修改失败')

    # 返回前端
    return jsonify(errno=RET.OK,errmsg='操作成功')



# 显示个人中心主页
@profile_blue.route('/user_info')
@user_login_data
def user_info():
    if not g.user:
        return redirect('/')

    data = {
        "user_info":g.user.to_dict()
    }
    return render_template('./news/user.html',data=data)
