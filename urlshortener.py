from flask import Flask
from pymongo import MongoClient
from flask_restful import reqparse, abort, Api, Resource
app = Flask(__name__)
client = MongoClient("mongodb+srv://sourMadMan:4HV2Y7Bq91VruPKi@cluster0.jmeohut.mongodb.net/?retryWrites=true&w=majority")
db = client.flask_db
urls = db.URLs
app = Flask(__name__)
api = Api(app)
