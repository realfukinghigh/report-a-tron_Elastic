from os import path
import secrets
import json


class Config(object):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_NAME = "reportatronSession"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    ENV = "production"

    secret_key = secrets.token_hex(512)
    SECRET_KEY = secret_key


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ENV = "staging"
    secret_key = secrets.token_hex(512)
    SECRET_KEY = secret_key


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ENV = "development"
    SECRET_KEY = 'development_key'

class TestingConfig(Config):
    TESTING = True
    ENV = "testing"
    SECRET_KEY = 'testing_key'

class StaticValues:
    abspath = path.abspath(__file__)
    dirname = path.dirname(abspath)
    config_path = str(dirname) + "//config.json"

    with open(config_path, "r") as infile:
    	config_file = json.loads(infile.read())
    infile.close()
