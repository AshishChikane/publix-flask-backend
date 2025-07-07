from Config.db import db
from sqlalchemy.sql import func

class InvalidPings(db.Model):
    __tablename__ = 'tbl_invalid_pings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    s_id = db.Column(db.Integer)
    campaign_id = db.Column(db.Integer)
    ping_type = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now())

    # Relationships can be added if needed
