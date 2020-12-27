from flask import Flask
from flask_restful import Resource, Api
from pymongo import MongoClient

# import resources
from auth import signup, login

mongo = MongoClient("mongodb://mongo:27017")
db = mongo.get_database("test")

app = Flask(__name__)
api = Api(app)

api.add_resource(signup, "/v1/auth/signup",  resource_class_kwargs={"db": db})
api.add_resource(login, "/v1/auth/login", resource_class_kwargs={"db": db})

if __name__ == '__main__':
    app.run(port=3000,host="0.0.0.0",debug=True)