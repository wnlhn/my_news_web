# 问句天几高，心中志比天更高
from flask import current_app
from flask import g, jsonify
from flask import redirect
from flask import render_template
from flask import request

from main_info.response_code import RET
from main_info.utils.common import user_login_data
from . import profile_blue

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
