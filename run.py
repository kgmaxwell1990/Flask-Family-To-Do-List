import os
from flask import Flask, redirect, render_template, request
from random import choice
import json
from pymongo import MongoClient
from bson.objectid import ObjectId

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
    tasks = load_user_tasks_from_mongo(username, member)
    return render_template("member_page.html", tasks=tasks, username=username, member=member)

@app.route("/<username>/<member>/new_task_form")
def render_task_form(username, member):
    return render_template("add_task.html", username=username, member=member)
    
@app.route("/<username>/<member>/submit_form", methods=["POST"])
def add_task(username,member):
    category_name = request.form.get("category_name")
    task_name = request.form.get("task_name")
    task_description = request.form.get("task_description")
    due_date = request.form.get("due_date")
    is_urgent = request.form.get("is_urgent")
    task = {"category_name": category_name,
            "task_name": task_name,
            "task_description": task_description,
            "due_date": due_date,
            "is_urgent": is_urgent
    }
            
    save_user_tasks_from_mongo(username,member,task)
    return redirect(username + "/" + member)
    
@app.route("/<username>/<member>/<task_name>/delete_task")
def delete_task(username, member, task_name):
    with MongoClient(MONGODB_URI) as conn:
        db = conn[MONGODB_NAME]
        selected_member = db[username].find_one({'name':member})
        if len(selected_member['task_list']) == 1:
            if task_name == selected_member['task_list'][0]["task_name"]:
                del selected_member['task_list'][0]
        
        for x in range(len(selected_member['task_list']) -1):
            if task_name == selected_member['task_list'][x]["task_name"]:
                del selected_member['task_list'][x]

        db[username].save(selected_member)
    
    return redirect(username + "/" + member)
    
@app.route("/<username>/<member>/<task_name>/edit_task", methods=['GET', 'POST'])
def edit_task(username, member, task_name):
    if request.method==("POST"):
        return "You submitted changes"
    else:
        return render_template("edittask.html")

    
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






































if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)