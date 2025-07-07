from Config.db import db

class CountryList(db.Model):
    __tablename__ = 'tbl_country'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country_id = db.Column(db.Integer)
    locale = db.Column(db.String(255))
    code = db.Column(db.String(255))
    name = db.Column(db.String(255))
    prefix = db.Column(db.String(255))
    status = db.Column(db.SmallInteger, default=0)  # TINYINT → SmallInteger
    time_zone = db.Column(db.String(255), nullable=True)

    # Add relationships if needed
