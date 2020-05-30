import os 

class Config():
    SECRET_KEY = 'gentlecare'
    socket_location = "/var/run/mysqld/mysqld.sock"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/gentlecare"
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@178.62.66.6/gentlecare"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    





