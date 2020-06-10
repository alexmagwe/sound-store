import os
basedir=os.path.abspath(os.path.dirname(__name__))


class Config():
    FLASK_APP=os.path.join(basedir,'margie','setup.py')
    SECRET_KEY ='20661143fd81501206948abe1df6ce38'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/vault.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False