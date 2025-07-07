from Config.db import db
from sqlalchemy.sql import func

class LocationList(db.Model):
    __tablename__ = 'tbl_location_list'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    
    site_uuid = db.Column(db.String(255))
    site_id = db.Column(db.String(255))
    site_name = db.Column(db.String(255))
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('tbl_publisher_users.id')
    )

    address_line = db.Column(db.Text)
    site_area = db.Column(db.String(255))
    
    site_city = db.Column(
        db.Integer,
        db.ForeignKey('tbl_cities_list.id')
    )

    site_state = db.Column(
        db.Integer,
        db.ForeignKey('tbl_states_list.id')
    )

    site_country = db.Column(
        db.Integer,
        db.ForeignKey('tbl_country.id')
    )

    site_code = db.Column(db.String(255))
    latitude = db.Column(db.String(255))
    longitude = db.Column(db.String(255))
    site_tags = db.Column(db.Text)

    cid = db.Column(
        db.Integer,
        db.ForeignKey('tbl_venue_category.id'),
        nullable=False
    )

    pid = db.Column(
        db.Integer,
        db.ForeignKey('tbl_publisher.id'),
        nullable=False
    )

    network = db.Column(
        db.Integer,
        db.ForeignKey('tbl_network.id')
    )

    is_enabled = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
