from Config.db import db

class AdScreenMapping(db.Model):
    __tablename__ = 'tbl_ad_schedular'

    ad_id = db.Column(db.Integer)

    day = db.Column(db.String(255))  # Adjust length as needed

    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
