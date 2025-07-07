from Config.db import db
from sqlalchemy.sql import func

class AdvertiserPlanX(db.Model):
    __tablename__ = 'tbl_advertiser_planx'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)

    planx_uuid = db.Column(db.String(255))
    planx_name = db.Column(db.String(255))

    brand_id = db.Column(db.Integer, db.ForeignKey('tbl_brands.id'))
    advertiser_id = db.Column(db.Integer, db.ForeignKey('tbl_advertiser.id'))

    user_id = db.Column(db.Integer)

    planx_age_type = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
