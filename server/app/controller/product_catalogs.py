from app.model.product_catalogs import ProductCatalogs
from app.controller import product_brands
from app import response, app, db
from datetime import datetime, timedelta
from flask import request
import math

def getAllProductCatalogs():
    try:
        catalog_list = ProductCatalogs.query.all()
        data = []
        for catalog in catalog_list:
            data.append({
                'id': catalog.id,
                'product_name': catalog.product_name,
                'type': catalog.type,
                'price': catalog.price,
                'image': catalog.image,
                'sold_item': catalog.sold_item,
                'brand_id': catalog.brand_id,
                'brand_info': product_brands.singleTransform(int(catalog.brand_id))
            })
        return response.ok(data, "success fetch data")
    except Exception as error:
        print(f'Failed to connect: {error}')

def getAllProductCatalogsAdmin():
    try:
        page = int(request.args.get('page', 1))
        limit = 5
        offset = (page - 1) * limit if (page - 1) * limit == 0 else (page - 1) * limit
        catalogs = ProductCatalogs.query.all()
        total_data = len(catalogs)
        total_pages = math.ceil(total_data / limit)
        
        catalog_list = ProductCatalogs.query.offset(offset).limit(limit).all()
        data = []
        for catalog in catalog_list:
            data.append({
                'id': catalog.id,
                'product_name': catalog.product_name,
                'type': catalog.type,
                'price': catalog.price,
                'image': catalog.image,
                'sold_item': catalog.sold_item,
                'brand_id': catalog.brand_id,
                'brand_info': product_brands.singleTransform(int(catalog.brand_id))
            })
        return response.okAdmin(data, total_pages, "success fetch data")
    except Exception as error:
        print(f'Failed to connect: {error}')

def getProductCatalogCatalogById(id):
    try:
        catalog = ProductCatalogs.query.filter_by(id=id).first()
        if not catalog:
            return response.badRequest([], "id not found")

        data = {
                'id': catalog.id,
                'product_name': catalog.product_name,
                'type': catalog.type,
                'price': catalog.price,
                'image': catalog.image,
                'sold_item': catalog.sold_item
        }

        return response.ok([data], "success fetch data")
    except Exception as error:
        print(f'Failed to connect: {error}')

def getProductCatalogByBrandId(id):
    try:
        catalog_list = ProductCatalogs.query.filter_by(brand_id=id).all()
        if not catalog_list:
            return response.badRequest([], "id not found")

        data = []
        for catalog in catalog_list:
            data.append({
                'id': catalog.id,
                'product_name': catalog.product_name,
                'type': catalog.type,
                'price': catalog.price,
                'image': catalog.image,
                'sold_item': catalog.sold_item
            })

        return data
    except Exception as error:
        print(f'Failed to connect: {error}')

def insertProductCatalog():
    try:
        name = request.json['product_name']
        type_pdk = request.json['type']
        brand_id = request.json['brand_id']
        image = request.json['image']
        price = request.json['price']
        sold_item = request.json['sold_item']

        catalog = ProductCatalogs(product_name=name, type=type_pdk, image=image, price=price, sold_item=sold_item, brand_id=brand_id)
        db.session.add(catalog)
        db.session.commit()
        return response.ok([], "Catalogs added successfully")
    except Exception as error:
        print(f'Failed to connect: {error}')

def updateProductCatalog(id):
    try:
        catalog = ProductCatalogs.query.filter_by(id=id).first()
        if not catalog:
            return response.badRequest([], "catalog not found")

        # Update catalog fields if present in the request JSON
        if 'product_name' in request.json:
            catalog.product_name = request.json['product_name']
        if 'type' in request.json:
            catalog.type = request.json['type']
        if 'image' in request.json:
            catalog.image = request.json['image']
        if 'price' in request.json:
            catalog.price = request.json['price']
        if 'sold_item' in request.json:
            catalog.sold_item = request.json['sold_item']
        if 'brand_id' in request.json:
            catalog.brand_id = request.json['brand_id']

        catalog.updated_at = datetime.utcnow()
        db.session.commit()

        return response.ok([], "Success update data")
    except Exception as error:
        print(f'Failed to connect: {error}')
        # return response.internalServerError([], "Failed to update user data")

def deleteProductCatalog(id):
    try:
        catalog = ProductCatalogs.query.filter_by(id=id).first()
        if not catalog:
            return response.badRequest([], "Catalog not found")

        db.session.delete(catalog)
        db.session.commit()

        return response.ok([], "Success delete catalog")
    except Exception as error:
        print(f'Failed to connect: {error}')
        return response.internalServerError([], "Failed to delete catalog")