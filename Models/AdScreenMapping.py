from Config.db import db

class AdScreenMapping(db.Model):
    __tablename__ = 'tbl_ad_screen_mapping'

    ad_id = db.Column(db.Integer)
    location_id = db.Column(db.Integer)
    s_id = db.Column(db.Integer)

    is_publix_approved = db.Column(db.Boolean, default=False)
    is_publisher_approved = db.Column(db.Boolean, default=False)
