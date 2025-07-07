from Config.db import db
from sqlalchemy.sql import func

class AdvertiserPublisherMapping(db.Model):
    __tablename__ = 'tbl_advertiser_publisher_mapping'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)

    advertiser_id = db.Column(db.Integer, db.ForeignKey('tbl_advertiser.id'))
    publisher_id = db.Column(db.Integer, db.ForeignKey('tbl_publisher.id'))

    is_publisher_sent = db.Column(db.Integer, default=0)   # 1 - Pending, 2 - Approve, 3 - Reject, 4 - Delete
    is_advertiser_sent = db.Column(db.Integer, default=0)  # 1 - Pending, 2 - Approve, 3 - Reject, 4 - Delete

    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
