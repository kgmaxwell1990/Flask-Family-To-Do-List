import os
from flask import Flask, redirect, render_template, request
from random import choice
import json
from pymongo import MongoClient

MONGODB_URI = os.environ.get("MONGODB_URI")
MONGODB_NAME = os.environ.get("MONGODB_NAME")

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/login")
def login():
    username = request.args.get("username")
    return redirect(username) 

@app.route("/<username>")
def get_userpage(username):
    members = load_members_from_mongo(username)
    return render_template("userpage.html", username=username, members=members)      

@app.route("/add_member")
def add_member():
    member = request.args.get("member")
    username = request.args.get("username")
    add_to_mongo(username, member)
    return redirect(username)  
    
    
def add_to_mongo(username, member):
    with MongoClient(MONGODB_URI) as conn:
        db = conn[MONGODB_NAME]
        collection = db[username]
        collection.insert({'name': member, 'list': []})
        
def load_members_from_mongo(username):
    with MongoClient(MONGODB_URI) as conn:
        db = conn[MONGODB_NAME]
        collection = db[username]
        users = db.collection_names()
        if username in users:
            user_members = collection.find()
            return user_members
        

# @app.route("/user.html" )
# def user():
#     items = load_list("data/list.json")    
#     welcome = choice(welcome_messages)
#     return render_template("daddy.html", msg=welcome, tasks=items)


# welcome_messages = ["Hi", "Hello", "Bonjour"]

# def load_list(filename):
#     if os.path.exists(filename):
#         with open(filename, "r") as f:
#             data = f.read()
#             items = json.loads(data)
#     else:
#         items = []
        
#     return items

# def save_list(filename, items):
#     with open(filename, "w") as f:
#         data = json.dumps(items)
#         f.write(data)































if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)