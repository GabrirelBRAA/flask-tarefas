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
from flask_cors import CORS, cross_origin
cors = CORS(app)

ACCESS_EXPIRES = timedelta(hours=2)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': f'redis://:{os.environ['REDIS_PASSWORD']}@{os.environ['REDIS_URL']}/0'})

from views.UserViews import user_views
from views.TaskViews import task_views

app.register_blueprint(user_views)
app.register_blueprint(task_views)

@app.route('/')
@cross_origin()
def hello_world():
    return 'Hello World! API is healthy!'
