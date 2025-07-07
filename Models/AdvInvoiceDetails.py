from Config.db import db
from sqlalchemy.sql import func

class AdvInvoiceStatus(db.Model):
    __tablename__ = 'tbl_adv_invoice_details'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)

    campaign_id = db.Column(db.Integer)
    invoice_number = db.Column(db.Integer)

    total_locations = db.Column(db.Integer)
    total_screens = db.Column(db.Integer)
    total_ads = db.Column(db.Integer)
    total_ad_plays = db.Column(db.Integer)
    total_play_duration = db.Column(db.Integer)

    taxable_amount = db.Column(db.Float)

    invoice_date = db.Column(db.DateTime, server_default=func.now())
    due_date = db.Column(db.DateTime)
    po_date = db.Column(db.DateTime)

    po_number = db.Column(db.String(255))
    invoice_url = db.Column(db.Text)

    tcgst = db.Column(db.Float)
    tsgst = db.Column(db.Float)
    tigst = db.Column(db.Float)

    platform_amount = db.Column(db.Float)

    pcgst = db.Column(db.Float)
    psgst = db.Column(db.Float)
    pigst = db.Column(db.Float)

    total_overall_value = db.Column(db.Float)

    tx_id = db.Column(db.String(255))
    tx_amt = db.Column(db.Float)
    tds_amt = db.Column(db.Float)

    tx_date = db.Column(db.DateTime)
    tx_url = db.Column(db.Text)
