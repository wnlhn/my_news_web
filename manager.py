# 问句天几高，心中志比天更高
from flask import Flask
from flask import session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from config import redis,config_dic

app = Flask(__name__)



# 根据用户传入的值自动选择模式
config = config_dic['develope']
# 开启CSRFProtect
CSRFProtect(app)
# 加载配置信息
app.config.from_object(config)
# 创建数据库对象
db = SQLAlchemy(app)
redis_store = redis.StrictRedis(host=config.REDIS_HOST,port=config.REDIS_PORT,decode_responses=True)
# 使用Session关联app
Session(app)
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
    return 'hello world'

if __name__ == '__main__':
    manager.run()