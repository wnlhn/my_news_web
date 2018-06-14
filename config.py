# 问句天几高，心中志比天更高
import logging
import redis


class Config(object):
    """工程的配置信息"""
    DEBUG = True
    # Mysql数据库配置信息
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql@localhost:3306/information'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 数据库内容发送改变之后,自动提交
    # Redis数据库配置信息
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    # flask_session 配置信息
    SESSION_TYPE = 'redis'  # 指定session存放在session中
    SESSION_USE_SIGNER = True # 让cookie中的session_id 被加密签名处理
    SESSION_REDIS = redis.StrictRedis(REDIS_HOST,REDIS_PORT) #指定存放的redis实力
    PERMANENT_SESSION_LIFETIME = 86400 # session的有效期，单位是秒  默认有效期是一个月
    SECRET_KEY = 'dsfkjlgkd'
    level = logging.DEBUG

class Product_model(Config):
    DEBUG = False
    level = logging.ERROR
    pass


class Develope_model(Config):
    pass


class Testing_model(Config):
    pass


config_dic = {
    "product":Product_model,
    'develope':Develope_model,
    'testing':Testing_model
}