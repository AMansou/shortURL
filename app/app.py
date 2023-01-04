# ########################################Imports#######################################################
import os
import boto3
from flask import Flask, jsonify, request,redirect
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




# import boto3


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
