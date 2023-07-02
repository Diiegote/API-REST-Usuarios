from decouple import config
class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = config('MYSQL_HOST')
    MYSQL_USER= config('MYSQL_USER')
    MYSQL_PASSWORD= config('MYSQL_PASSWORD')
    MYSQL_DB= config('MYSQL_DB')


config = {
    'development': DevelopmentConfig
}


