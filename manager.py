# 问句天几高，心中志比天更高
import logging

from flask import current_app
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from main_info import create_app,db


app = create_app('develope')
# 数据库迁移
manager = Manager(app)
Migrate(app,db)
manager.add_command('db',MigrateCommand)

@app.route('/')
def index():
    # redis_store.set('name','liuneng')
    # name = redis_store.get('name')
    # print(name)
    # session['name'] = 'laiwang'
    # name = session.get('name')
    # print(name)
    logging.debug('debug')
    logging.info('info')
    logging.debug('debug')
    logging.warn('warn')
    logging.fatal('big_fatal')
    current_app.logger.debug('current_app_debug')

    return 'hello world'

if __name__ == '__main__':
    manager.run()