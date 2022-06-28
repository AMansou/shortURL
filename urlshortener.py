########################################Imports#######################################################
from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from json import loads
from flask_restful import reqparse, abort, Api, Resource
########################################Constants#####################################################
BASE=64 ## this project will map the decimal id numbers of url database entries into base64
MAP = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-" ## these are the characters to be mapped
## Note the more you increase the base the shorter the URL becomes. 64 was picked because that's
## The number of characters we want to map the id into.
######################Connecting to Mongodv and initializing the Flask app############################
app = Flask(__name__)
client = MongoClient("mongodb+srv://sourMadMan:4HV2Y7Bq91VruPKi@cluster0.jmeohut.mongodb.net/?retryWrites=true&w=majority")
db = client.flask_db
urls = db.URLs
app = Flask(__name__)
api = Api(app)
######################################################################################################
## nextId is the id of the next element to be stored in the database. nextId is incremented every time
## we add a new row to the collection. When the server restarts for whatever reason, it retrieves
## the previous value of nextId from the database and adds 1 to it. If the collection is empty,
## nextId is initialized to 0. We use the id to map it to base64 and thus get a unique short URL.
#####################################################################################################
nextId=0
if "URLs" in db.list_collection_names():
    nextId=loads(dumps(list(urls.find().sort([('_id', -1)]).limit(1))[0]))['_id']+1

#########################################Useful Functions############################################
def idToShortURL(id): ## Map Id into base64
	shortURL = ""
	# for each digit find the base 64
	while(id > 0):
		shortURL += MAP[id % BASE]
		id //= BASE
	# reversing the shortURL
	return shortURL[len(shortURL): : -1]
## Invoke this if user enters an unknown path
def abortion(pth):
        abort(404, message="Doesn't exist :(".format(pth))
############################Add arguments entered by the user to the parser#########################
parser = reqparse.RequestParser()
parser.add_argument('alias')
parser.add_argument('url')
###############################Create a different class for each endpoint###########################
class Create(Resource):
    def post(self):
        global nextId # Do not create a local variable called nextId. Make it global.
        args = parser.parse_args()
        urls.insert_one({'_id':nextId,'url': args['url'], 'short': idToShortURL(nextId)})
        nextId+=1
        return "http://localhost:5000/"+idToShortURL(nextId)
###
## find the short url in the database and redirect the user to the original URL if found
##
class Redir(Resource):
    def get(self,pth):
        rslt=loads(dumps(urls.find({'short':pth})))
        if rslt==[]:
            abortion(pth)
        return redirect(rslt[0]['url'])

##
## setup the Api resource routing here
##
api.add_resource(Create, '/create')
api.add_resource(Redir, '/<pth>')
if __name__ == '__main__':
    app.run(debug=True)
