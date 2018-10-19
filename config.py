import os


class Config:
    """
    Describes the general configurations
    """
    SECRET_KEY = os.environ.get ('SECRET_KEY')
    DATABASE_PASS = os.environ.get('DATABASE_PASS')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_PHOTOS_DEST = 'app/static/photos'

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get ('MAIL_PASSWORD')
    SUBJECT_PREFIX = 'kellers-blog'
    SENDER_EMAIL = 'muthonkel@gmail.com'

    # Simple MDE configurations
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True

    @staticmethod
    def init_app(app):
        pass


class ProdConfig(Config):
    """
    child class of config
    activate when you go to production mode
    """
    DATABASE_PASS = os.environ.get('DATABASE_PASS')
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class DevConfig(Config):
    """
    child class of Config
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://kellen:kellen@localhost/blogger'
    DEBUG = True


config_options = {
    'development': DevConfig,
    'production': ProdConfig,

}
