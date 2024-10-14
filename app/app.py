from flask import Flask, request, jsonify
import os
app = Flask(__name__)

from database import init_db, db_session
import bcrypt

init_db()

from models.User import User
from models.Task import Task, TaskStatus, TaskScheme

from pydantic import parse_obj_as

from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from typing import List
from datetime import timedelta

from flask_caching import Cache

ACCESS_EXPIRES = timedelta(hours=2)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': f'redis://:{os.environ['REDIS_PASSWORD']}@{os.environ['REDIS_URL']}/0'})

from views.UserViews import user_views
from views.TaskViews import task_views

app.register_blueprint(user_views)
app.register_blueprint(task_views)

@app.route('/')
def hello_world():
    return 'Hello, World!, from flask app!'

"""
@app.post('/create-user')
def create_user():
    request.json['name']
    salt=bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(request.json['password'].encode('utf-8'), salt)
    user = User(
        name=request.json['name'],
        password_hash=hashed_password,
        password_salt=salt, #Field inútil
    )
    db_session.add(user)
    db_session.commit()
    return str(user) #Validate this with pydantic

@app.post('/login')
def login():
    name = request.json['name']
    user = User.query.filter(User.name == name).first()
    if bcrypt.checkpw(request.json['password'].encode('utf-8'), user.password_hash):
        additional_claims = {"name": name}
        return create_access_token(identity=user.id, additional_claims=additional_claims)
    return jsonify({"msg": "Bad username or password"}), 401
"""

"""
@app.post('/task/create')
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    task = Task(
        user_id=user_id,
        description=request.json['description'],
        status=TaskStatus.pending,
    )
    db_session.add(task)
    db_session.commit()
    return TaskScheme.model_validate(task).model_dump(mode='json')

@app.get('/task/list')
@jwt_required()
def listTasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter(Task.user_id == user_id).all()
    tasks_json = parse_obj_as(List[TaskScheme], tasks)
    return [task.model_dump(mode='json') for task in tasks_json]

@app.post('/task/<int:task_id>/delete')
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    Task.query.filter(Task.user_id == user_id, Task.id == task_id).delete()
    db_session.commit()

    return ('', 204)

@app.route('/task/<int:task_id>/update', methods=['PATCH'])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter(Task.user_id == user_id, Task.id == task_id).first()
    task.status = request.json['status']
    
    db_session.commit()
    return TaskScheme.model_validate(task).model_dump(mode='json')

@app.get('/task/<int:task_id>/detail')
@jwt_required()
def task_detail(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter(Task.user_id == user_id, Task.id == task_id).first()
    
    return TaskScheme.model_validate(task).model_dump(mode='json')

@app.route('/env')
def env():
    return os.environ['SECRET']
"""