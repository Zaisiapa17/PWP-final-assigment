from app.model.todos import Todos
from app.controller import users
from app import response, app, db
from datetime import datetime
from flask import request, jsonify
from flask_jwt_extended import *

@jwt_required()
def index():
    try:
        id = request.args.get('user_id')
        todo = Todos.query.filter_by(user_id=id).all()
        print(todo)
        data = transform(todo)
        return response.ok(data, "succes")
    except Exception as error:
        print(f'Failed to connect: {error}')

def insertTodo():
    try:
        todo = request.json['todo']
        description = request.json['description']
        user_id = request.json['user_id']

        todo = Todos(user_id = user_id, todo = todo, description = description)
        db.session.add(todo)
        db.session.commit()
        return response.ok([], "Todo added successfully")
    except Exception as error:
        print(f'Failed to connect: {error}')

def updateTodo(id):
    try:
        todo = Todos.query.filter_by(id=id).first()
        if not todo:
            return response.badRequest([], "id not found")

        if 'todo' in request.json:
            todo.todo = request.json['todo']

        if 'description' in request.json:
            todo.description = request.json['description']

        todo.updated_at = datetime.utcnow()
        db.session.commit()

        return response.ok([], "Success update data")
    except Exception as error:
        print(f'Failed to connect: {error}')

def getTodoById(id):
    try:
        todo = Todos.query.filter_by(id=id).first()
        if not todo:
            return response.badRequest([], "id not found")

        data = singleTransform(todo)

        return response.ok([data], "success fetch data")
    except Exception as error:
        print(f'Failed to connect: {error}')

def deleteTodo(id):
    try:
        todo = Todos.query.filter_by(id=id).first()
        if not todo:
            return response.badRequest([], "todo not found")

        db.session.delete(todo)
        db.session.commit()

        return response.ok([], "Success delete todo")
    except Exception as error:
        print(f'Failed to connect: {error}')
        return response.internalServerError([], "Failed to delete todo")

def transform(values):
    array = []
    for value in values:
        array.append(singleTransform(value))
    return array

def singleTransform(values):
    data = {
            'id': values.id,
            'user_id': values.user_id,
            'todo': values.todo,
            'description': values.description,
            'created_at': values.created_at,
            'updated_at': values.updated_at,
            'users': users.singleTransform(values.users, withTodo = False)
        }
    return data