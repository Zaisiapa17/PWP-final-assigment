from app import db
from datetime import datetime

class ProductBrands(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    brand_name = db.Column(db.String(225), nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<ProductBrands {}>'.format(self.product_brands)