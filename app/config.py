import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    INSTANCE_DIR = os.path.join(BASE_DIR, '..', 'instance')
    
    os.makedirs(INSTANCE_DIR, exist_ok=True)
    
    DATABASE_PATH = os.path.join(INSTANCE_DIR, "database.db")
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Debug prints (remove these after fixing)
    print(f"Database URI: {SQLALCHEMY_DATABASE_URI}")
    print(f"Instance Directory: {INSTANCE_DIR}")
    print(f"Database path: {DATABASE_PATH}")