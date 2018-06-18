# 问句天几高，心中志比天更高
from flask import current_app
from flask import g, jsonify
from flask import redirect
from flask import render_template
from flask import request

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


@profile_blue.route('/')










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
