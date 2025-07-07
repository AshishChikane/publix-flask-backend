from Config.db import db

class PlanXAge(db.Model):
    __tablename__ = 'tbl_plan_age_group'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    planx_id = db.Column(db.Integer)
    age_group = db.Column(db.String(255))
    is_available = db.Column(db.SmallInteger, default=0)  # TINYINT → SmallInteger

    # Relationships can be added if needed
