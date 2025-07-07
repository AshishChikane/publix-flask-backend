from Config.db import db

class AdvertiserBank(db.Model):
    __tablename__ = 'tbl_advertiser_bank_details'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)

    bank_name = db.Column(db.String(255))
    account_number = db.Column(db.String(255))
    ifsc_code = db.Column(db.String(255))
    bank_branch = db.Column(db.String(255))
    swift_code = db.Column(db.String(255))
