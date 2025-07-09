from Config.db import db
from sqlalchemy.sql import func

class AdvertiserUser(db.Model):
    __tablename__ = 'tbl_advertiser_users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))
    email_id = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    password = db.Column(db.String(255))
    otp = db.Column(db.Integer)
    role_id = db.Column(db.Integer)
    email_token = db.Column(db.String(255))
    is_email_verified = db.Column(db.Boolean, default=True)
    is_allowed = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    brand_ids = db.Column(db.Text)
    is_owner = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=func.now())

    def __repr__(self):
        return f"<AdvertiserUser(id={self.id}, email_id='{self.email_id}')>"
