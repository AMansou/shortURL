# ########################################Imports#######################################################
# from flask import Flask, render_template, request, url_for, redirect
# from flask_restful import reqparse, abort, Api, Resource
import boto3
# import os
# ########################################Constants#####################################################
BASE=64 ## this project will map the decimal id numbers of url database entries into base64
MAP = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-" ## these are the characters to be mapped
INPUT="input.txt"
## Note the more you increase the base the shorter the URL becomes. 64 was picked because that's
## The number of characters we want to map the id into.
######################Connecting to Mongodv and initializing the Flask app############################
DDB = boto3.client('dynamodb', region_name='us-east-1')
# app = Flask(__name__)
# api = Api(app)
# #########################################Useful Functions############################################
def idToShortURL(id): ## Map Id into base64
	shortURL = ""
	# for each digit find the base 64
	while(id > 0):
		shortURL += MAP[id % BASE]
		id //= BASE
	# reversing the shortURL
	return shortURL[len(shortURL): : -1]
def ShortURLtoId(shortURL):
    """
    converts base62 number to decimal
    """
    ret = 0
    for i in range(len(shortURL)-1,-1,-1): #apo 61 os 0
        ret = ret + MAP.index(shortURL[i]) * (62**(len(shortURL)-i-1))
    return ret
## Invoke this if user enters an unknown path
def abortion(pth):
        return pth+" does not exist :("
# def isAlias(alias):
#     if len(alias)>5 or len(alias)<1 or loads(dumps(urls.find({'alias':alias})))!=[]:
#         return False
#     for i in alias:
#         if i not in MAP:
#             return False
#     return True
# ############################Add arguments entered by the user to the parser#########################
# parser = reqparse.RequestParser()
# parser.add_argument('alias')
# parser.add_argument('url')
# ###############################Create a different class for each endpoint###########################
# class testing(Resource):
#     # def get(self,pth):
# 	# 	DDB.put_item(TableName="short-url", Item={'ID': {'N': 0},'url': {'S': "fb.com"},'alias': {'S':'a'}})
# 	# 	# record = DDB.get_item(Key={'alias': {'S': 'a'}},TableName="short-url")['Item']['url']['S']
#     #     return ShortURLtoId(idToShortURL(5))
# 	# 	# return record
# 	def get(self,pth):
# 		DDB.put_item(TableName="short-url", Item={'ID': {'N': '0'},'url': {'S': "fbj.com"},'alias': {'S':'a'}})
# 		record = DDB.get_item(Key={'ID': {'N': '0'}},TableName="short-url")
# 		return len(record)
# ###
# ## find the short url in the database and redirect the user to the original URL if found
# ##
# class Redir(Resource):
#     # def get(self,pth):
# 	# 	x=0
#     #     return ShortURLtoId(pth)
# 	def get(self,pth):
		# record = DDB.get_item(Key={'ID': {'N': str(ShortURLtoId(pth))}},TableName="short-url")
		# if len(record)==1:
		# 	abortion(pth)
		# else:
		# 	return redirect(record["Item"]["url"]['S'])
#
# class Create(Resource):
# 	def post(self):
		# args = parser.parse_args()
		# if args['alias']==None:
		# 	nextId=0
		# 	while True:
		# 		record=DDB.get_item(Key={'ID': {'N': str(nextId)}},TableName="short-url")
		# 		if len(record)==1:
		# 			DDB.put_item(TableName="short-url", Item={'ID': {'N': str(nextId)},'url': {'S': args["url"]},'alias': {'S':idToShortURL(nextId)}})
		# 			return "Success! " + args['url'] + ' Is mapped to ' + idToShortURL(nextId)
		# 			break
		# 		nextId+=1
		# else:
		# 	record=DDB.get_item(Key={'ID': {'N': str(ShortURLtoId(args['alias']))}},TableName="short-url")
		# 	if len(record)==1:
		# 		DDB.put_item(TableName="short-url", Item={'ID': {'N': str(ShortURLtoId(args['alias'])) },'url': {'S': args["url"]},'alias': {'S':args['alias']}})
		# 		return "Success! " + args['url'] + ' Is mapped to ' + args['alias']
		# 	else:
		# 		return "Mission failed"
		#
		#
		#
		# 	return "ngubu"
#
# ##
# ## setup the Api resource routing here
# ##
# api.add_resource(Create, '/create')
# # api.add_resource(Alias, '/alias/<pth>')
# api.add_resource(Redir, '/<pth>')
# # api.add_resource(testing, '/<pth>')
# if __name__ == '__main__':
#     app.run(threaded=True,host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))










































import os

# import boto3

from flask import Flask, jsonify, request,redirect
app = Flask(__name__)

#client = boto3.client('dynamodb', region_name='us-east-1')
dynamoTableName = 'short-url'

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/<string:pth>")
def get_url(pth):
	record = DDB.get_item(Key={'ID': {'N': str(ShortURLtoId(pth))}},TableName="short-url")
	if len(record)==1:
		return pth+" Does not exist :("
	else:
		return redirect(record["Item"]["url"]['S'])



@app.route("/create", methods=["POST"])
def create_url():
	args=request.form
	if 'alias' not in args.keys():
		nextId=0
		while True:
			record=DDB.get_item(Key={'ID': {'N': str(nextId)}},TableName="short-url")
			if len(record)==1:
				DDB.put_item(TableName="short-url", Item={'ID': {'N': str(nextId)},'url': {'S': args["url"]},'alias': {'S':idToShortURL(nextId)}})
				return "Success! " + args['url'] + ' Is mapped to ' + idToShortURL(nextId)
				break
			nextId+=1
	else:
		record=DDB.get_item(Key={'ID': {'N': str(ShortURLtoId(args['alias']))}},TableName="short-url")
		if len(record)==1:
			DDB.put_item(TableName="short-url", Item={'ID': {'N': str(ShortURLtoId(args['alias'])) },'url': {'S': args["url"]},'alias': {'S':args['alias']}})
			return "Success! " + args['url'] + ' Is mapped to ' + args['alias']
		else:
			return "Mission failed"





if __name__ == '__main__':
    app.run(threaded=True,host='0.0.0.0',port=5000)
