from Config.db import db

class AdMedia(db.Model):
    __tablename__ = 'tbl_ad_media'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)

    ad_id = db.Column(db.Integer)

    screen_resolution_width = db.Column(db.Integer)
    screen_resolution_height = db.Column(db.Integer)

    media_url = db.Column(db.String(255)) 
