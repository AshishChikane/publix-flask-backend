from Config.db import db
from sqlalchemy.sql import func
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Publisher(db.Model):
    __tablename__ = 'tbl_publisher'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    publisher_uuid = db.Column(db.String(255), default=generate_uuid)
    company_name = db.Column(db.String(255))
    brand_name = db.Column(db.String(255))
    user_type = db.Column(db.Integer, default=1)
    company_email = db.Column(db.String(255))
    company_number = db.Column(db.String(255))
    company_address = db.Column(db.Text)
    currency = db.Column(db.Integer)
    access_key = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=func.now())
    authorized_name = db.Column(db.String(255))
    authorized_mobile = db.Column(db.String(255))
    authorized_email = db.Column(db.String(255))
    bank_id = db.Column(db.Integer)
    kyc_id = db.Column(db.Text)
    platform_fees = db.Column(db.Float, default=10.0)
    gst_number = db.Column(db.String(255))
    is_blocked = db.Column(db.Boolean, default=False)
    code_identity = db.Column(db.Text)

    # Relationships (if needed)
    screens = db.relationship('Screen', backref='publisher_details', lazy=True)  # Relationship with Screen model we just created
