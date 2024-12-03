class Config:
    SECRET_KEY = b'\x1df\xa1<\xbbC[q\xe2R\x948\xf4P{\x0c\xb4\xcc\xffh\x95-\x86\xe9+kx\x9f\x08T\xed\x17'
    DEBUG = True
    PORT = 8000
    SQLALCHEMY_DATABASE_URI = 'sqlite:///household.db' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
