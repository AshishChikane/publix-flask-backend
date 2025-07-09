from Config.db import db
from sqlalchemy.sql import func

class Brand(db.Model):
    __tablename__ = 'tbl_brands'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    brand_uuid = db.Column(db.String(255))
    brand_name = db.Column(db.String(255))

    advertiser_id = db.Column(
        db.Integer,
        # db.ForeignKey('tbl_advertiser.id'),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        # db.ForeignKey('tbl_brand_category.id'),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        # db.ForeignKey('tbl_advertiser_users.id'),
        nullable=False
    )

    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
