from flask import request
from flask_restful import Resource
from cerberus import Validator
from argon2 import PasswordHasher
import python_jwt as jwt, jwcrypto.jwk as jwk, datetime

ph = PasswordHasher()

key = jwk.JWK.generate(kty='RSA', size=2048)

signup_schema = {
  "email": {
    "type": "string",
    "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    "required": True
  },
  "password": {
    "type": "string",
    "required": True,
    "minlength": 6,
    "maxlength": 30
  }
}

login_schema = {
  "email": {
    "type": "string",
    "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    "required": True
  },
  "password": {
    "type": "string",
    "required": True,
    "minlength": 6,
    "maxlength": 30
  }
}

signup_validator = Validator()

login_validator = Validator()

# function to see if email registered
def check_email(db, email):
  c = db.get_collection("users")
  
  user = c.find_one({"email": email})

  if not user:
    return False
  else:
    return True

# signup endpoint
class signup(Resource):

  def __init__(self, db):
    self.db = db

  def post(self):
    data = request.get_json()
    validation = signup_validator.validate(data, signup_schema)

    if validation == False:
      return {"statusCode":400, "error": signup_validator.errors}, 400

    email_exist = check_email(self.db, data["email"])

    if email_exist == True:
      return {"statusCode":400, "error": "Email exists"}, 400

    try:

      hashed_pass = ph.hash(data["password"])

      new_user = {
        "email": data["email"],
        "hash": hashed_pass
      }

      c = self.db.get_collection("users")

      user_id = c.insert_one(new_user).inserted_id

      payload = {"uid": str(user_id)}
      token = jwt.generate_jwt(payload, key, 'PS256', datetime.timedelta(hours=24))

      return {"access_token": token}, 200

    except:
      return {"statusCode": 500, "error": "Internal server error"}

# login endpoint
class login(Resource):
  def __init__(self, db):
    self.db = db

  def post(self):

    data = request.get_json()
    validation = login_validator.validate(data, login_schema)

    if validation == False:
      return {"statusCode":400, "error": signup_validator.errors}, 400

    try:

      c = self.db.get_collection("users")

      user = c.find_one({"email": data["email"]})

      if not user:
        return {"statusCode": 400, "error": "Invalid email or password"}, 400

      matches = ph.verify(user["hash"], data["password"])

      if not matches:
        return {"statusCode": 400, "error": "Invalid email or password"}, 400

      payload = {"uid": str(user["_id"])}
      token = jwt.generate_jwt(payload, key, 'PS256', datetime.timedelta(hours=24))

      return {"access_token": token}, 200

    except:
      return {"statusCode": 500, "error": "Internal server error"}
