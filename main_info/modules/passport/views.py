# 问句天几高，心中志比天更高
from flask import current_app
from flask import make_response
from flask import request
from main_info.utils.captcha.captcha import captcha

from my_news_web.main_info import constants
from my_news_web.main_info import redis_store
from . import passprot_blue

@passprot_blue.route('/')
def get_image_code():
    # 1获取请求参数
    cur_id = request.args.get('cur_id')
    pre_id = request.args.get('pre_id')
    # 2生成图片验证码
    name,text,image_data = captcha.generate_captcha()
    # 3 保存到redis  凡是跟数据库打交道都需要try
    try:
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