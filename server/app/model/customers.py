from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Customers(db.Model):
    
    def setPassword(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def checkPassword(self, password):
        return check_password_hash(self.password, password)
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(230), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=True)
    phone = db.Column(db.BigInteger, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<customers {}>'.format(self.name)