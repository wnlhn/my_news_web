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


if __name__ == '__main__':
    print(app.url_map)
    manager.run()