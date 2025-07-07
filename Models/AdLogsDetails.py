from Config.db import db
from sqlalchemy.sql import func

class ActiveLogs(db.Model):
    __tablename__ = 'tbl_active_logs_detail'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)

    campaign_id = db.Column(db.Integer)
    ad_id = db.Column(db.Integer)
    screen_id = db.Column(db.Integer)

    lost_impression_count = db.Column(db.Integer)
    complete_impression_count = db.Column(db.Integer)
    total_impression_count = db.Column(db.Integer)

    peak_hour_complete_count = db.Column(db.Integer)
    non_peak_hour_complete_count = db.Column(db.Integer)

    peak_hour_lost_count = db.Column(db.Integer)
    non_peak_hour_lost_count = db.Column(db.Integer)

    logs = db.Column(db.Text)

    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
