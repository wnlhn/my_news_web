# 问句天几高，心中志比天更高
import random
from datetime import datetime, timedelta

from flask import current_app
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from main_info import create_app,db,models
from main_info.models import User

app = create_app('develope')
# 数据库迁移
manager = Manager(app)
Migrate(app,db)
manager.add_command('db',MigrateCommand)


# 创建管理员账号
@manager.option("-u",'--username',dest='username')
@manager.option("-p",'--password',dest='password')
def create_admin(username,password):

    admin = User()
    admin.mobile = username
    admin.password = password
    admin.is_admin = True
    admin.nick_name = username

    try:
        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return ('数据库操作失败')
    print('创建成功！')




#创建测试用户
def create_users():
    user_list = []
    now = datetime.now()
    for i in range(0,1000):
        user = User()
        user_name = '186%08d' % i
        user.nick_name = user_name
        user.mobile = user_name
        user.password_hash = 'pbkdf2:sha256:50000$M2iRqfGh$87c687e8b0e91b13c6273eb3a1138bb4a66d768790bb3813d62a34a064c1ce47'
        user.last_login = now - timedelta(seconds=random.randint(0,3600*24*31))
        user_list.append(user)
    # 打开应用上下文
    with app.app_context():
        try:
            db.session.add_all(user_list)
            db.session.commit()
        except Exception as e:
            # current_app.logger.error(e)
            return ('数据库操作失败')
    print('创建1000测试用户成功')


if __name__ == '__main__':
    # print(app.url_map)
    # create_users()
    manager.run()