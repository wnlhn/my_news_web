# 问句天几高，心中志比天更高
from flask import Flask
from flask import session
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

app = Flask(__name__)


class Config(object):
    """工程的配置信息"""
    DEBUG = True
    # Mysql数据库配置信息
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql@localhost:3306/information'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Redis数据库配置信息
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    # flask_session 配置信息
    SESSION_TYPE = 'redis'  # 指定session存放在session中
    SESSION_USE_SIGNER = True # 让cookie中的session_id 被加密签名处理
    SESSION_REDIS = redis.StrictRedis(REDIS_HOST,REDIS_PORT) #指定存放的redis实力
    PERMANENT_SESSION_LIFETIME = 86400 # session的有效期，单位是秒  默认有效期是一个月
    SECRET_KEY = 'dsfkjlgkd'

# 开启CSRFProtect
CSRFProtect(app)
# 加载配置信息
app.config.from_object(Config)
# 创建数据库对象
db = SQLAlchemy(app)
redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT,decode_responses=True)
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