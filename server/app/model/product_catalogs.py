from app import db
from datetime import datetime
from app.model.product_brands import ProductBrands

class ProductCatalogs(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(225), nullable=False)
    type = db.Column(db.String(225), nullable=False)
    image = db.Column(db.String(225), nullable=False)
    price = db.Column(db.BigInteger, nullable=False)
    sold_item = db.Column(db.BigInteger, nullable=False)
    brand_id = db.Column(db.BigInteger, db.ForeignKey(ProductBrands.id))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<ProductCatalogs {}>'.format(self.product_name)