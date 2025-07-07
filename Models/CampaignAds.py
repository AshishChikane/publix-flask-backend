from Config.db import db

class CampaignAds(db.Model):
    __tablename__ = 'tbl_campaign_ads'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    ad_uuid = db.Column(db.String(255))
    ad_title = db.Column(db.String(255))
    cid = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    ad_plays = db.Column(db.Integer)
    media_duration = db.Column(db.Float)  # DOUBLE → Float in SQLAlchemy
    media_type = db.Column(db.String(255))
    media_ext = db.Column(db.String(255))
    is_active = db.Column(db.SmallInteger, default=0)  # TINYINT → SmallInteger
    status = db.Column(db.Integer, default=0)
    is_added = db.Column(db.SmallInteger, default=0)

    # Relationships (if any) can be defined here
