from Config.db import db

class PlanxGender(db.Model):
    __tablename__ = 'tbl_planx_gender'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    planx_id = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(255), nullable=False)
    male_ratio = db.Column(db.Integer, nullable=True)
    female_ratio = db.Column(db.Integer, nullable=True)

    # Add relationships if needed
