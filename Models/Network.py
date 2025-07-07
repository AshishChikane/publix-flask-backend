from Config.db import db
from sqlalchemy.sql import func

class Network(db.Model):
    __tablename__ = 'tbl_network'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    network_uuid = db.Column(db.String(255))
    network_name = db.Column(db.String(255))
    network_description = db.Column(db.String(255))
    publisher_id = db.Column(
        db.Integer,
        db.ForeignKey('tbl_publisher.id')  # Foreign key reference to tbl_publisher.id
    )
    is_active = db.Column(db.SmallInteger, default=1)  # TINYINT → SmallInteger
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now())

    # Optional: relationship to Publisher model
    publisher = db.relationship('Publisher', backref='networks', lazy=True)
