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

@app.route("/<username>/add_member", methods=["POST"])
def add_member(username):
    member = request.form.get("member")
    add_member_to_mongo(username, member)
    return redirect(username)  
    
@app.route("/<username>/<member>")
def get_family_member(username, member):
    # tasks = [
    #     {
    #         "task_name": "Buy Laptop",
    #         "task_description": "Need for bootcamp",
    #         "due_date": "21/6/2018",
    #         "urgent": False
    #     },
    #     {
    #         "task_name": "Learn To Code",
    #         "task_description": "Coding in Python",
    #         "due_date": "30/6/2018",
    #         "urgent": True
    #     }
    tasks = load_user_tasks_from_mongo(username, member)
    print("*******")
    print(tasks)
    return render_template("member_page.html", tasks=tasks, username=username, member=member)

@app.route("/<username>/<member>/new_task_form")
def render_task_form(username, member):
    return render_template("add_task.html", username=username, member=member)
    
    
@app.route("/<username>/<member>/submit_form", methods=["POST"])
def add_task(username,member):
    task_name = request.form.get("task_name")
    task_description = request.form.get("task_description")
    due_date = request.form.get("due_date")
    
    task = {"task_name": task_name,
            "task_description": task_description,
            "due_date": due_date}
            
    save_user_tasks_from_mongo(username,member,task)
    return redirect(username + "/" + member)
    
    
    
    

def add_member_to_mongo(username, member):
    with MongoClient(MONGODB_URI) as conn:
        db = conn[MONGODB_NAME]
        collection = db[username]
        collection.insert({'name': member, 'task_list': []})
        
def load_members_from_mongo(username):
    with MongoClient(MONGODB_URI) as conn:
        db = conn[MONGODB_NAME]
        collection = db[username]
        users = db.collection_names()
        if username in users:
            user_members = collection.find()
            return user_members
            

def load_user_tasks_from_mongo(username, member):
    with MongoClient(MONGODB_URI) as conn:
        db = conn[MONGODB_NAME]
        list = db[username].find_one({'name':member})
        return list['task_list']
        
def save_user_tasks_from_mongo(username,member,task):
    with MongoClient(MONGODB_URI) as conn:
        db = conn[MONGODB_NAME]
        find_document = db[username].find_one({'name':member})
        find_document['task_list'].append(task)
        db[username].save(find_document)

# def load_list_items_from_mongo(username, list_name):
#     with MongoClient(MONGODB_URI) as conn:
#         db = conn[MONGODB_NAME]
#         return db[username].find({'name':list_name})
 
 
 
 
 
 
 
 
    
# @app.route('/insert_task', methods=['POST'])
# def add_task():
#     member = request.args.get("member")
#     username = request.args.get("username")
    
    
#     add_to_mongo(username, member)
#     return redirect(username)  





# @app.route('/insert_task', methods=['POST'])
# def insert_task():
#     if tasks in list:
#         tasks =  mongo.db.tasks
#         tasks.insert_one(request.form.to_dict())
#         return redirect(url_for('get_tasks'))

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