# 问句天几高，心中志比天更高
import random
import re
from datetime import datetime

from flask import current_app, jsonify
from flask import make_response
from flask import request
from flask import session
from main_info.utils.captcha.captcha import captcha

from my_news_web.main_info import constants, db
from my_news_web.main_info import redis_store
from my_news_web.main_info.libs.yuntongxun.sms import CCP
from my_news_web.main_info.models import User
from my_news_web.main_info.response_code import RET
from . import passprot_blue
# from main_info.utils.response_code import RET

# 登陆用户
# 请求路径: /passport/login
# 请求方式: POST
# 请求参数: mobile,password
# 返回值: errno, errmsg
@passprot_blue.route('/login',methods=['POST'])
def login():
    """
    1 获取参数
    2 验证参数
    3 通过手机号取出用户对象
    4 判断用户对象是否存在
    5 判断是否信息正确
    6 记录登陆状态
    7 返回前端
    :return:
    """""
    # 1获取参数
    dict_data = request.json
    mobile = dict_data['mobile']
    password = dict_data['password']

    # 2验证参数
    if not all([mobile,password]):
        return jsonify(errno=RET.PARAMERR,errmsg='参数不完整')
    if not re.match('1[356789]\d{9}',mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号格式不正确')

    # 3通过手机号取出用户对象
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR ,errmsg='数据库查询异常')

    # 4判断用户对象是否存在
    if not user:
        return jsonify(errno=RET.NODATA, errmsg='用户不存在')

    # 5判断是否信息正确
    if not user.check_passowrd(password):
        return jsonify(errno=RET.DATAERR, errmsg='密码输入错误')

    # 6记录登陆状态(使用session存储,下次访问直接去除)
    session['user_id'] = user.id
    session['mobile'] = user.mobile
    session['nick_name'] = user.nick_name


    try:
        # 7更新登陆时间
        user.last_login = datetime.now()
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg='提交到数据库失败')

    # 8返回前端
    return jsonify(errno=RET.OK, errmsg='登陆成功!')





# 注册用户
# 请求路径: /passport/register
# 请求方式: POST
# 请求参数: mobile, sms_code,password
# 返回值: errno, errmsg
@passprot_blue.route('/register', methods=['POST'])
def register():
    """
    1.获取参数
    2.校验参数(为空校验,手机号格式校验)
    3.通过手机号取出redis中的短信验证码
    4.判断是否过期
    5.判断是否相等
    6.创建用户对象,设置属性
    7.保存到数据库
    8.返回前端页面
    :return:
    """
    # 1.获取参数
    dict_data = request.json
    mobile = dict_data.get('mobile')
    sms_code = dict_data.get('sms_code')
    password = dict_data.get('password')

    # 2.校验参数(为空校验, 手机号格式校验)
    if not all([mobile,sms_code,password]):
        return jsonify(errno=RET.PARAMERR,errmsg='参数不完整')
    if not re.match('1[356789]\d{9}',mobile):
        return jsonify(errno=RET.DATAERR,errmsg='手机号格式不正确')

    # 3.通过手机号取出redis中的短信验证码
    try:
        redis_sms_code = redis_store.get('msg_code:%s' % mobile).decode()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='获取短信验证码异常')
    # 4.判断是否过期
    if not redis_sms_code:
        return jsonify(errno=RET.NODATA, errmsg="短信验证码过期")
    # 5.判断是否相等
    if not redis_sms_code == sms_code:
        print(sms_code,type(sms_code))
        print(redis_sms_code,type(redis_sms_code))
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码填写错误")

    # 6.创建用户对象, 设置属性
    user = User()
    user.nick_name = mobile
    user.mobile = mobile
    # 使用property属性  高大上
    user.password = password
    # low version
    # user.password_hash = user.jiami_secret(password)
    # 7.保存到数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="用户保存异常")

    # 8.返回前端页面
    return jsonify(errno=RET.OK,errmsg='注册成功')




#短信验证码
# 请求路径: /passport/sms_code
# 请求方式: POST
# 请求参数: mobile, image_code,image_code_id
# 返回值: errno, errmsg
@passprot_blue.route('/sms_code', methods=['POST'])
def get_sms_code():
    """
    1.获取参数,request.data,  json.loads(json)
    2.校验参数为空情况
    3.验证手机号格式
    4.通过image_code_id取出redis中的图片验证码
    5.判断取出的图片验证码是否过期
    6.判断两者图片验证码是否相等
    7.生成短信验证码
    8.调用云通讯发送(手机号,短信验证码,有效期,模板id)
    9.保存到redis
    10.返回前端
    :return:
    """
     # 1.获取参数,request.data,  json.loads(json)
    dict_data = request.json
    mobile = dict_data.get('mobile')
    image_code_id = dict_data.get('image_code_id')
    image_code = dict_data.get('image_code')
    # print(image_code)

     # 2.校验参数为空情况
    if not all([mobile,image_code,image_code_id]):
        return jsonify(errno=RET.PARAMERR,errmsg='参数不完整')

     # 3.验证手机号格式
    if not re.match('1[356789]\d{9}',mobile):
        return jsonify(errno=RET.DATAERR,errmsg='手机号格式错误')

     # 4.通过image_code_id取出redis中的图片验证码
    try:
        redis_image_code = redis_store.get('image_code:%s'%image_code_id).decode(   )
        current_app.logger.error(redis_image_code)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='查找图片验证码失败')

     # 5.判断取出的图片验证码是否过期
    if not redis_image_code:
        return jsonify(errno=RET.NODATA,errmsg='图片验证码已经过期')

     # 6.判断两者图片验证码是否相等
    if not redis_image_code.lower() == image_code.lower():
        # print(redis_image_code)
        # current_app.logger.error(redis_image_code)
        # current_app.logger.error(image_code)
        return jsonify(errno=RET.DATAERR,errmsg='图片验证码输入错误')

     # 7.生成短信验证码
    sms_code = '%06d'%random.randint(0,999999)
     # 8.调用云通讯发送(手机号,短信验证码,有效期,模板id)
    # ccp = CCP()
    # result = ccp.send_template_sms(mobile,[sms_code,5],1)
    # if result == -1:
    #     return jsonify(errno=RET.THIRDERR,errmsg='短信验证码发送失败')
    current_app.logger.debug('短信验证码是:%s'%sms_code)
     # 9.保存到redis
    try:
        redis_store.set('msg_code:%s'%mobile,sms_code,constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='短信保存到数据库失败')

     # 10.返回前端

    return jsonify(errno=RET.OK,errmsg='发送成功!')


#图片验证码
@passprot_blue.route('/')
def get_image_code():
    # 1获取请求参数
    cur_id = request.args.get('cur_id')
    pre_id = request.args.get('pre_id')
    # 2生成图片验证码
    name,text,image_data = captcha.generate_captcha()
    # 3 保存到redis  凡是跟数据库打交道都需要try
    try:
        current_app.logger.error(text)
        redis_store.set('image_code:%s'%cur_id,text,constants.IMAGE_CODE_REDIS_EXPIRES)
        if redis_store.get('image_code:%s'%pre_id):
            redis_store.delete('image_code:%s'%pre_id)
    except Exception as e:
        current_app.logger.error(e)
    # 4 返回图片验证码
    # 设置返回的类型为图片
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/jpg'
    return response