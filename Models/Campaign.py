from Config.db import db
from sqlalchemy.sql import func

class Campaign(db.Model):
    __tablename__ = 'tbl_campaign'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    campaign_uuid = db.Column(db.String(255))
    campaign_name = db.Column(db.String(255))

    advertiser_id = db.Column(
        db.Integer,
        db.ForeignKey('tbl_advertiser.id'),
    )

    brand_id = db.Column(
        db.Integer,
        db.ForeignKey('tbl_brands.id'),
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('tbl_advertiser_users.id'),
    )

    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    time_schedule = db.Column(db.Text)

    # 0 - Pending, 1 - Active, 2 - Complete, 4 - Pause
    is_active = db.Column(db.Integer, default=0)

    # 0 - New, 1 - InReview, 2 - Update, 3 - Approve, 4 - Reject, 5 - New Ad
    status = db.Column(db.Integer, default=0)

    ad_plays = db.Column(db.Integer)
    cost = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    adv_invoice_status = db.Column(db.Integer)
    pb_invoice_status = db.Column(db.Integer)
    adv_platform_fees = db.Column(db.Float)

    is_blockchain_enabled = db.Column(db.Integer, default=0)
    campaign_mode = db.Column(db.String(255))
