# 问句天几高，心中志比天更高
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

    return 'hello world'
