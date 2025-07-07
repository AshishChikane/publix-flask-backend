from Config.db import db

class CampaignScreenMapping(db.Model):
    __tablename__ = 'tbl_campaign_screen_mapping'

    campaign_id = db.Column(db.Integer)
    location_id = db.Column(db.Integer)
    s_id = db.Column(db.Integer)
    is_publix_approved = db.Column(db.SmallInteger, default=0)  # TINYINT → SmallInteger
    is_publisher_approved = db.Column(db.SmallInteger, default=0)
    cost = db.Column(db.Integer)
    ads = db.Column(db.BigInteger)  # BIGINT → BigInteger

    # If needed, you can add ForeignKey relationships here
