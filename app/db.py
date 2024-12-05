import os
from dotenv import load_dotenv
from flask_pymongo import PyMongo
from pymongo_inmemory import MongoClient
import sys

def init_db():
    if "pytest" in sys.modules:
        client = MongoClient()  # No need to provide host
        return client
    else:
        mongo = PyMongo()
        return mongo


def get_db(app, mongo):
    APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
    dotenv_path = os.path.join(APP_ROOT, '.env')
    load_dotenv(dotenv_path)
    if "pytest" in sys.modules:
        return mongo
    else:
        app.config["MONGO_URI"] = os.getenv('database')    
        mongo.init_app(app)


