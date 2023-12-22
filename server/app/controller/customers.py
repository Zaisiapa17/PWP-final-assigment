from app.model.customers import Customers
from app import response, app, db
from datetime import datetime
from flask import request


def getAllCustomers():
    try:
        customer_list = Customers.query.all()
        data = []
        for customer in customer_list:
            data.append({
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                'phone': customer.phone,
                'password': customer.password
            })
        return response.ok(data, "success fetch data")
    except Exception as error:
        print(f'Failed to connect: {error}')

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

def insertCustomer():
    try:
        name = request.json['name']
        email = request.json['email']
        phone = request.json['phone']
        password = request.json['password']

        customer = Customers(name=name, email=email, phone=phone, password=password)
        db.session.add(customer)
        db.session.commit()
        return response.ok([], "customer added successfully")
    except Exception as error:
        print(f'Failed to connect: {error}')

def updateCustomer(id):
    try:
        customer = Customers.query.filter_by(id=id).first()
        if not customer:
            return response.badRequest([], "customer not found")

        # Update customer fields if present in the request JSON
        if 'name' in request.json:
            customer.name = request.json['name']
        if 'email' in request.json:
            customer.email = request.json['email']
        if 'phone' in request.json:
            customer.phone = request.json['phone']
        if 'password' in request.json:
            customer.password = request.json['password']

        customer.updated_at = datetime.utcnow()
        db.session.commit()

        return response.ok([], "Success update data")
    except Exception as error:
        print(f'Failed to connect: {error}')
        # return response.internalServerError([], "Failed to update user data")

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