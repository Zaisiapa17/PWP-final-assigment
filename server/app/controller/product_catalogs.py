from app.model.product_catalogs import ProductCatalogs
from app import response, app, db
from datetime import datetime, timedelta
from flask import request

def getAllProductCatalogs():
    try:
        users_list = ProductCatalogs.query.all()
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

def getProductCatalogCatalogById(id):
    try:
        user = ProductCatalogs.query.filter_by(id=id).first()
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

def insertProductCatalog():
    try:
        name = request.json['product_name']
        type_pdk = request.json['type']
        brand_id = request.json['brand_id']

        catalog = ProductCatalogs(product_name=name, type=type_pdk, brand_id=brand_id)
        db.session.add(catalog)
        db.session.commit()
        return response.ok([], "Catalogs added successfully")
    except Exception as error:
        print(f'Failed to connect: {error}')

def updateProductCatalog(id):
    try:
        user = ProductCatalogs.query.filter_by(id=id).first()
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

def deleteProductCatalog(id):
    try:
        user = ProductCatalogs.query.filter_by(id=id).first()
        if not user:
            return response.badRequest([], "User not found")

        db.session.delete(user)
        db.session.commit()

        return response.ok([], "Success delete user")
    except Exception as error:
        print(f'Failed to connect: {error}')
        return response.internalServerError([], "Failed to delete user")