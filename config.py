import os

class Config:
    # Format: mysql+pymysql://username:password@hostname/databasename
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Pampi2012$@localhost/crm'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'super_secret_key_for_session_security'