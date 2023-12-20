from app.model.users import Users
from app import response, app, db
from datetime import datetime, timedelta
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import *

@jwt_required(refresh=True)
def refresh():
    try:
        user = get_jwt_identity()
        new_token = create_access_token(identity=user, fresh=False)

        return response.ok({'token_access': new_token}, "success!")
    except Exception as error:
        print(f'Failed to connect: {error}')

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

        expires = timedelta(days=1)
        expires_refresh = timedelta(days=3)
        access_token = create_access_token(data, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(data, expires_delta=expires_refresh)

        
        return response.ok({'data': data, 'token_access': access_token, 'token_refresh': refresh_token}, "Login successful")
    except Exception as error:
        print(f'Failed to connect: {error}')

def getAllProductBrands():
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

def getProductBrandById(id):
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

def insertProductBrand():
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

def updateProductBrand(id):
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

def deleteProductBrand(id):
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