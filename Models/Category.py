from Config.db import db

class CategoryList(db.Model):
    __tablename__ = 'tbl_venue_category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    category_name = db.Column(db.String(255))  # Default length if not specified

    # No timestamps or relationships needed here
