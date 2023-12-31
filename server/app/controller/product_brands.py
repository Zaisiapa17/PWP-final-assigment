from app.model.product_brands import ProductBrands
from app import response, app, db
from app.controller import product_catalogs
from datetime import datetime
from flask import request


def getAllProductBrands():
    try:
        brands_list = ProductBrands.query.all()
        data = []
        for brand in brands_list:
            data.append({
                'id': brand.id,
                'brand_name': brand.brand_name,
                'brand_address': brand.brand_address,
                'brand_catalogs': product_catalogs.getProductCatalogByBrandId(brand.id)
            })
        return response.ok(data, "success fetch data")
    except Exception as error:
        print(f'Failed to connect: {error}')

def getProductBrandById(id):
    try:
        brand = ProductBrands.query.filter_by(id=id).first()
        if not brand:
            return response.badRequest([], "id not found")

        data = {
            'id': brand.id,
            'brand_name': brand.brand_name,
            'brand_address': brand.brand_address
        }

        return response.ok([data], "success fetch data")
    except Exception as error:
        print(f'Failed to connect: {error}')

def insertProductBrand():
    try:
        name = request.json['brand_name']
        brand_address = request.json['brand_address']

        brand = ProductBrands(brand_name=name, brand_address=brand_address)
        db.session.add(brand)
        db.session.commit()
        return response.ok([], "brand added successfully")
    except Exception as error:
        print(f'Failed to connect: {error}')

def updateProductBrand(id):
    try:
        brand = ProductBrands.query.filter_by(id=id).first()
        if not brand:
            return response.badRequest([], "Brand not found")

        # Update brand fields if present in the request JSON
        if 'brand_name' in request.json:
            brand.brand_name = request.json['brand_name']
        if 'brand_address' in request.json:
            brand.brand_address = request.json['brand_address']

        brand.updated_at = datetime.utcnow()
        db.session.commit()

        return response.ok([], "Success update data")
    except Exception as error:
        print(f'Failed to connect: {error}')
        # return response.internalServerError([], "Failed to update user data")

def deleteProductBrand(id):
    try:
        brand = ProductBrands.query.filter_by(id=id).first()
        if not brand:
            return response.badRequest([], "brand not found")

        db.session.delete(brand)
        db.session.commit()

        return response.ok([], "Success delete brand")
    except Exception as error:
        print(f'Failed to connect: {error}')
        return response.internalServerError([], "Failed to delete brand")

def singleTransform(brand_id):
        brand = ProductBrands.query.filter_by(id=brand_id).first()
        data = {
            'id': brand.id,
            'brand_name': brand.brand_name,
            'brand_address': brand.brand_address
        }

        return data