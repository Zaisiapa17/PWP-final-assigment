from app.model.users import Users
from app import response, app, db
from datetime import datetime
from flask import request

def login():
    try:
        name = request.json['name']
        password = request.json['password']

        user = Users.query.filter_by(name=name).first()
        if not user:
            return response.badRequest([], "User not found")

        if not user.checkPassword(password):
            return response.badRequest([], "Password incorrect")

        data = {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }

        return response.ok([data], "Login successful")
    except Exception as error:
        print(f'Failed to connect: {error}')

def getAllusers():
    try:
        users_list = Users.query.all()
        data = []
        for user in users_list:
            data.append({
                'id': user.id,
                'name': user.name,
                'email': user.email
            })
        return response.ok(data, "success fetch data")
    except Exception as error:
        print(f'Failed to connect: {error}')

def getUserById(id):
    try:
        user = Users.query.filter_by(id=id).first()
        if not user:
            return response.badRequest([], "id not found")

        data = {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }

        return response.ok([data], "success fetch data")
    except Exception as error:
        print(f'Failed to connect: {error}')

def insertUser():
    try:
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']

        users = Users(name=name, email=email)
        users.setPassword(password)
        db.session.add(users)
        db.session.commit()
        return response.ok([], "User added successfully")
    except Exception as error:
        print(f'Failed to connect: {error}')

def updateUser(id):
    try:
        user = Users.query.filter_by(id=id).first()
        if not user:
            return response.badRequest([], "User not found")

        # Update user fields if present in the request JSON
        if 'name' in request.json:
            user.name = request.json['name']
        if 'email' in request.json:
            user.email = request.json['email']
        if 'password' in request.json:
            user.setPassword(request.json['password'])

        user.updated_at = datetime.utcnow()
        db.session.commit()

        return response.ok([], "Success update data")
    except Exception as error:
        print(f'Failed to connect: {error}')
        # return response.internalServerError([], "Failed to update user data")

def singleTransform(users, withTodo=True):
    data = {
    'id': users.id,
    'name': users.name,
    'email': users.email
    }
    if withTodo:
        todos = []
        for i in users.todos:
            todos.append({
            'id': i.id,
            'todo': i.todo,
            'description': i.description,
            })
        data['todos'] = todos
    return data

def deleteUser(id):
    try:
        user = Users.query.filter_by(id=id).first()
        if not user:
            return response.badRequest([], "User not found")

        db.session.delete(user)
        db.session.commit()

        return response.ok([], "Success delete user")
    except Exception as error:
        print(f'Failed to connect: {error}')
        return response.internalServerError([], "Failed to delete user")