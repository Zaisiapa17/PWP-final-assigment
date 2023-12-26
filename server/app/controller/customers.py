from app.model.customers import Customers
from app import response, app, db
from datetime import datetime
from flask import request
import math
from flask_jwt_extended import *


def getAllCustomers():
    try:
        customer_list = Customers.query.all()
        data = []
        for customer in customer_list:
            data.append({
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                'phone': customer.phone
            })
        return response.ok(data, "success fetch data")
    except Exception as error:
        print(f'Failed to connect: {error}')


@jwt_required()
def getAllCustomersAdmin():
    try:
        page = int(request.args.get('page', 1))
        limit = 5
        offset = (page - 1) * limit if (page - 1) * limit == 0 else (page - 1) * limit
        catalogs = Customers.query.all()
        total_data = len(catalogs)
        total_pages = math.ceil(total_data / limit)
        
        customer_list = Customers.query.offset(offset).limit(limit).all()
        data = []
        for customer in customer_list:
            data.append({
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                'phone': customer.phone
            })
        return response.okAdmin(data, total_pages, "success fetch data")
    except Exception as error:
        print(f'Failed to connect: {error}')

@jwt_required()
def getCustomerById(id):
    try:
        customer = Customers.query.filter_by(id=id).first()
        if not customer:
            return response.badRequest([], "id not found")

        data = {
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                'phone': customer.phone,
                'password': customer.password
        }

        return response.ok([data], "success fetch data")
    except Exception as error:
        print(f'Failed to connect: {error}')

@jwt_required()
def insertCustomer():
    try:
        name = request.form['kontact_name_add']
        email = request.form['kontact_email_add']
        phone = request.form['kontact_phone_add']
        password = request.form['kontact_password_add']

        customer = Customers(name=name, email=email, phone=phone)
        customer.setPassword(password)
        db.session.add(customer)
        db.session.commit()
        return response.ok([], "customer added successfully")
    except Exception as error:
        print(f'Failed to connect: {error}')

@jwt_required()
def updateCustomer(id):
    try:
        customer = Customers.query.filter_by(id=id).first()
        if not customer:
            return response.badRequest([], "customer not found")

        # Update customer fields if present in the request JSON
        if 'kontact_name_edit' in request.form and request.form['kontact_name_edit']:
            customer.name = request.form['kontact_name_edit']
        if 'kontact_email_edit' in request.form and request.form['kontact_email_edit']:
            customer.email = request.form['kontact_email_edit']
        if 'kontact_phone_edit' in request.form and request.form['kontact_phone_edit']:
            customer.phone = request.form['kontact_phone_edit']
        if 'kontact_password_edit' in request.form and request.form['kontact_password_edit']:
            customer.setPassword(request.form['kontact_password_edit'])

        customer.updated_at = datetime.utcnow()
        db.session.commit()

        return response.ok([], "Success update data")
    except Exception as error:
        print(f'Failed to connect: {error}')

@jwt_required()
def deleteCustomer(id):
    try:
        customer = Customers.query.filter_by(id=id).first()
        if not customer:
            return response.badRequest([], "customer not found")

        db.session.delete(customer)
        db.session.commit()

        return response.ok([], "Success delete customer")
    except Exception as error:
        print(f'Failed to connect: {error}')
        return response.internalServerError([], "Failed to delete customer")