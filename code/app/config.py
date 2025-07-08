import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'changeme')
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL', 'mysql+pymysql://user:password@db_message:3306/messages_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
