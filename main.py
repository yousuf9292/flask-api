from flask import Flask,jsonify,request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
import os

app = Flask(__name__)


jwt = JWTManager(app)
mongo = PyMongo(app)
db = mongo.db

app.config["MONGO_URI"]=os.environ['MONGO']
app.config["JWT_SECRET_KEY"]=os.environ['SECRET']


@app.route("/<username>/<email>/<password>",methods=['GET','POST'])
def registered(username,email,password):
    if db.registration.find_one({"_id":email}):
        return jsonify(email+" already registered")
    else:
        db.registration.insert_one({"username":username,"_id":email,"password":password})
        return jsonify(email+" got registered")

@app.route("/login/<email>/<password>",methods=['GET','POST'])
def login(email,password):
    if db.registration.find_one({"_id": email})["_id"]==email and \
            db.registration.find_one({"_id": email})["password"]==password:
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token)
    else:
        return jsonify("Wrong Credentials")


@app.route("/courses",methods=['GET'])
def courses():
    courses=db.courses.find()
    return jsonify([course for course in courses])

@app.route("/course/<courses>",methods=['GET','POST'])
def registered_course(courses):
    if db.courses.find_one({"_id":courses}):
        return jsonify(courses+" already registered")
    else:
        db.courses.insert_one({"_id":courses})
        return jsonify(courses+" got registered")



@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200