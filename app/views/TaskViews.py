
from models.Task import Task, TaskStatus, TaskScheme
from database import db_session
from pydantic import parse_obj_as
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from typing import List
from app import cache

task_views = Blueprint('task_views', __name__, url_prefix='/task')

@task_views.post('/create')
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    try:
        validated_task = TaskScheme.model_validate(request.json)
        task = Task(
            user_id=user_id,
            description=validated_task.description,
            status=validated_task.status,
        )
        db_session.add(task)
        db_session.commit()

        cache.clear()

        return TaskScheme.model_validate(task).model_dump(mode='json')
    except Exception as e:
        return jsonify(repr(e)), 400


@task_views.get('/list')
@cache.cached(timeout=50)
def listTasks():
    tasks = Task.query.all() #redis tem que ficar aqui
    tasks_json = parse_obj_as(List[TaskScheme], tasks)
    return [task.model_dump(mode='json') for task in tasks_json]

@task_views.post('/<int:task_id>/delete')
@jwt_required()
def delete_task(task_id):
    try:
        task = Task.query.filter(Task.id == task_id).first()

        if task is None:
            raise ValueError("Wrong id, task does not exist!")

        db_session.delete(task)
        db_session.commit()

    except Exception as e:
        return jsonify(repr(e)), 400

    cache.clear()

    return ('', 204)

@task_views.route('/<int:task_id>/update', methods=['PATCH'])
@jwt_required()
def update_task(task_id):
    try:
        if request.json['status'] is 1 or request.json['status'] is 2:
            task = Task.query.filter(Task.id == task_id).first()

            if task is None:
                raise ValueError("Wrong id, task does not exist!")

            task.status = TaskStatus(request.json['status'])
        
            db_session.commit()

            cache.clear()
            return TaskScheme.model_validate(task).model_dump(mode='json')
        else:
            raise ValueError("status is required! Must be a 1 'pending' or a 2 'done'")

    except Exception as e:
        return jsonify(repr(e)), 400
    

