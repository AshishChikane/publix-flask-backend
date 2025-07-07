from Config.db import db

class CityList(db.Model):
    __tablename__ = 'tbl_cities_list'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    city_name = db.Column(db.String(255))
    country_code = db.Column(db.String(255))
    state_code = db.Column(db.String(255))
    latitude = db.Column(db.String(255))
    longitude = db.Column(db.String(255))
    status = db.Column(db.SmallInteger, default=0)  # TINYINT → SmallInteger

    # Add relationships if needed
