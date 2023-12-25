from app.model.product_catalogs import ProductCatalogs
from app.controller import product_brands
from app import response, app, db
from datetime import datetime
from flask import request, jsonify
from werkzeug.utils import secure_filename
import math
import os

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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
        # Extracting data from form
        name = request.form['product_name_add']
        type_pdk = request.form['type_add']
        brand_id = request.form['brand_id_add']
        price = request.form['price_add']
        sold_item = request.form['sold_item_add']

        # Handling file upload
        if 'image_add' not in request.files:
            return jsonify(error="No file part"), 400

        file = request.files['image_add']

        if file.filename == '':
            return jsonify(error="No selected file"), 400

        if file and allowed_file(file.filename):
            # Save the file with a secure filename
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Create ProductCatalogs instance and add to the database
            catalog = ProductCatalogs(
                product_name=name,
                type=type_pdk,
                image=filename,
                price=price,
                sold_item=sold_item,
                brand_id=brand_id
            )
            
            db.session.add(catalog)
            db.session.commit()

            return jsonify(message="Product added successfully"), 200

        return jsonify(error="Invalid file type"), 400

    except Exception as error:
        print(f'Failed to connect: {error}')
        return jsonify(error="Internal server error"), 500


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