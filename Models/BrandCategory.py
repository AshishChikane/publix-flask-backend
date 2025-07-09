from Config.db import db 

class BrandCategory(db.Model):
    __tablename__ = 'tbl_brand_category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    brand_type = db.Column(db.String(255))

    def __repr__(self):
        return f"<BrandCategory(id={self.id}, brand_type='{self.brand_type}')>"
