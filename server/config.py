import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    HOST = str(os.environ.get("DB_HOST"))
    DATABASE = str(os.environ.get("DB_DATABASE"))
    USERNAME = str(os.environ.get("DB_USERNAME"))
    PASSWORD = str(os.environ.get("DB_PASSWORD"))
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + USERNAME + ':' + PASSWORD + '@' + HOST + '/' + DATABASE
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True
    JWT_SECRET_KEY = str(os.environ.get("JWT_SECRET"))
    UPLOAD_FOLDER = 'C:/Users/Alie/Documents/KAMPUS UTY/Semester 3/Pemrograman Web Praktek/final-assigment/server/files_uploaded/img'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}