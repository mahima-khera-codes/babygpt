import os
from dotenv import load_dotenv
from flask_pymongo import PyMongo
from pymongo_inmemory import MongoClient
import sys
from flask import g, request, jsonify

has_mongo = False
try:
    from pymongo import MongoClient
    from bson.objectid import ObjectId
    has_mongo = True   
except ModuleNotFoundError as e:
    pass

db_hosts = {}
def initDB(account_name, account_config):
    if "pytest" in sys.modules:
        client = MongoClient()  # No need to provide host
        return client.db
    else:
        if not has_mongo:
            return None
        
        global db_hosts
        if account_name not in db_hosts:
            if account_config["mongodb"]["host"] == None:
                if account_config["mongodb"]["db"] != None:
                    client = MongoClient(os.getenv('database'))
                    db_hosts[account_name] = client[account_config["mongodb"]["db"]]
                else:
                    return None
            else:
                client = MongoClient(account_config["mongodb"]["host"])
                db_hosts[account_name] = client[account_config["mongodb"]["db"]]
        return db_hosts[account_name]

