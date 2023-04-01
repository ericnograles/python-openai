import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://username:password@localhost/dbname'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HONEYCOMB_API_KEY = os.getenv("HONEYCOMB_API_KEY")
    HONEYCOMB_DATASET = os.getenv("HONEYCOMB_DATASET")
    # Add other configurations as needed
