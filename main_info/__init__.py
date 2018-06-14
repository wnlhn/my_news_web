# 问句天几高，心中志比天更高
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask import session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import redis,config_dic


db = SQLAlchemy()
redis_store = redis.StrictRedis()


def create_app(model):
    # 根据用户传入的值自动选择模式
    app = Flask(__name__)
    config = config_dic[model]
    # 开启CSRFProtect
    # CSRFProtect(app)
    # 加载配置信息
    app.config.from_object(config)
    # 生成日志文件
    log_file(config.level)
    # 创建数据库对象
    db.init_app(app)
    global redis_store
    redis_store = redis.StrictRedis(host=config.REDIS_HOST,port=config.REDIS_PORT,decode_responses=True)
    # 使用Session关联app
    Session(app)
    # 注册首页蓝图
    from main_info.modules.index import index_blue
    app.register_blueprint(index_blue)
    # 注册验证蓝图
    from main_info.modules.passport import passprot_blue
    app.register_blueprint(passprot_blue)


    return app

def log_file(level):
    # 设置日志的记录等级
    logging.basicConfig(level=level) # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)