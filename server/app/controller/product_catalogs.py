from app.model.product_catalogs import ProductCatalogs
from app.controller import product_brands
from app import response, app, db
from datetime import datetime
from flask import request, jsonify
from werkzeug.utils import secure_filename
import math
import os
from PIL import Image
import secrets
from flask_jwt_extended import *


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def crop_and_save_image(input_file, output_path, target_width, target_height):
    img = Image.open(input_file)
    
    # Calculate the aspect ratio of the target dimensions
    target_aspect_ratio = target_width / target_height
    
    # Calculate the aspect ratio of the original image
    original_aspect_ratio = img.width / img.height
    
    if original_aspect_ratio > target_aspect_ratio:
        # Crop the width
        new_width = int(target_height * original_aspect_ratio)
        img = img.resize((new_width, target_height), Image.LANCZOS)
        
        left_margin = (new_width - target_width) / 2
        right_margin = left_margin + target_width
        top_margin = 0
        bottom_margin = target_height
    else:
        # Crop the height
        new_height = int(target_width / original_aspect_ratio)
        img = img.resize((target_width, new_height), Image.LANCZOS)
        
        left_margin = 0
        right_margin = target_width
        top_margin = (new_height - target_height) / 2
        bottom_margin = top_margin + target_height
    
    # Crop the image
    cropped_img = img.crop((left_margin, top_margin, right_margin, bottom_margin))
    
    # Save the cropped image
    cropped_img.save(output_path)

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

@jwt_required()
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
                'sold_item': catalog.sold_item,
                'brand_id': catalog.brand_id,
                'brand_info': product_brands.singleTransform(int(catalog.brand_id))
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

@jwt_required()
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
            # Generate a random filename
            random_filename = secrets.token_hex(16)
            filename = 'cropped_' + random_filename + '.' + file.filename.rsplit('.', 1)[1].lower()
            
            # Save the cropped file with the random filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            crop_and_save_image(file, file_path, target_width=188, target_height=190)

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

@jwt_required()
def updateProductCatalog(id):
    try:
        catalog = ProductCatalogs.query.filter_by(id=id).first()
        if not catalog:
            return response.badRequest([], "Catalog not found")

        # Update catalog fields if present and not empty/undefined in the request JSON
        if 'product_name_edit' in request.form and request.form['product_name_edit']:
            catalog.product_name = request.form['product_name_edit']
            
        if 'type_edit' in request.form and request.form['type_edit']:
            catalog.type = request.form['type_edit']
            

        file = request.files['image_edit']
        if file.filename != '':

            if file and allowed_file(file.filename):
                # Generate a random filename
                random_filename = secrets.token_hex(16)
                filename = 'cropped_' + random_filename + '.' + file.filename.rsplit('.', 1)[1].lower()
                
                # Save the cropped file with the random filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                crop_and_save_image(file, file_path, target_width=188, target_height=190)

                catalog.image = filename
            else:
                return jsonify(error="Invalid file type"), 400
            
        if 'price_edit' in request.form and request.form['price_edit']:
            catalog.price = request.form['price_edit']
            
        if 'sold_item_edit' in request.form and request.form['sold_item_edit']:
            catalog.sold_item = request.form['sold_item_edit']
            
        if 'brand_id_edit' in request.form and request.form['brand_id_edit']:
            catalog.brand_id = request.form['brand_id_edit']

        catalog.updated_at = datetime.utcnow()
        db.session.commit()

        return response.ok([], "Success update data")
    except Exception as error:
        print(f'Failed to connect: {error}')

@jwt_required()
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