from Config.db import db
from sqlalchemy.sql import func

class AdvertiserUserActivity(db.Model):
    __tablename__ = 'tbl_advertiser_user_activity'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)

    user_id = db.Column(db.Integer)
    advertiser_id = db.Column(db.Integer)

    api_path = db.Column(db.String(255))    
    ip_address = db.Column(db.String(255))  
    action = db.Column(db.String(255))      

    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
