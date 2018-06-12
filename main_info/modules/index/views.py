# 问句天几高，心中志比天更高
from flask import current_app
from flask import render_template
from main_info import redis_store
from . import index_blue

@index_blue.route('/')
def index():
    # redis_store.set('name','liuneng')
    # name = redis_store.get('name')
    # print(name)
    # session['name'] = 'laiwang'
    # name = session.get('name')
    # print(name)
    # logging.debug('debug')
    # logging.info('info')
    # logging.debug('debug')
    # logging.warn('warn')
    # logging.fatal('big_fatal')
    # current_app.logger.debug('current_app_debug')
    # 注意点: 标记了templates为templates_folder之后会自动进入查找
    return render_template('news/index.html')

@index_blue.route('/favicon.ico')
def favicon_ico():
    return current_app.send_static_file('news/favicon.ico')