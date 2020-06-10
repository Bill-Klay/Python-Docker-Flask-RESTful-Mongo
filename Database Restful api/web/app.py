#!/usr/bin/python3

'''
Registeration of a user for 0 tokens
Each user gets 10 tokens
Store a sentence or quote on the database for 1 token
Retrieve the stored sentence on the database for 1 token
'''

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt


app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["Users"]

class Register(Resource):
    def post(self):
        #Get posted data by user
        postedData = request.get_json()
        
        #Get the data from json
        username =  postedData["username"]
        password = postedData["password"]

        #Hash password
        hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #Store username and password to the database
        users.insert({
            "Username": username,
            "Password": hashed,
            "Sentence": "",
            "Tokens": 5
        })

        retJson = {
            "status": 200,
            "msg": "Thank you for registering"
        }

        return jsonify(retJson)

def verify_pw(username, password):
    hashed = users.find({
        "Username": username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed) == hashed:
        return True
    else:
        return False

def count_tk(username):
    tokens = users.find({
        "Username": username
    })[0]["Tokens"]
    
    return tokens

class Store(Resource):
    def post(self):
        postedData = request.get_json()

        username =  postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        #Verify user
        checkPostedData = verify_pw(username, password)
        if not checkPostedData:
            retJson = {
                "status": 302,
                "message": "Incorrect Password"
            }
            return jsonify(retJson)

        #Verify tokens
        num_token = count_tk(username)
        if num_token < 0:
            retJson = {
                "status": 301,
                "message": "Insufficient tokens"
            }
            return retJson

        #Insert sentence
        users.update({
            "Username": username
        }, {
            "$set": {
                "Sentence": sentence,
                "Tokens": num_token - 1
            }
        })

        retJson = {
            "status": 200,
            "msg": "Sentence saved sucessfully"
        }
        return jsonify(retJson)

class Get(Resource):
    def post(self):
        postedData = request.get_json()
        username =  postedData["username"]
        password = postedData["password"]

        checkPostedData = verify_pw(username, password)
        if not checkPostedData:
            retJson = {
                "status": 302,
                "message": "Incorrect Password"
            }
            return jsonify(retJson)

        num_token = count_tk(username)
        if num_token < 0:
            retJson = {
                "status": 301,
                "message": "Insufficient tokens"
            }
            return retJson

        users.update({
            "Username": username
        }, {
            "$set": {
                "Tokens": num_token - 1
            }
        })

        sentence = users.find({
            "Username": username
        })[0]["Sentence"]

        retJson = {
            "status": 200,
            "sentence": sentence
        }

        return jsonify(retJson)

api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')

if __name__ == "__main__":
    app.run(host='0.0.0.0')