from Config.db import db

class PlanXProximity(db.Model):
    __tablename__ = 'tbl_planx_proximity_mapping'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    planx_id = db.Column(
        db.Integer,
        db.ForeignKey('tbl_advertiser_planx.id')  # ForeignKey to tbl_advertiser_planx.id
    )
    proximity_id = db.Column(
        db.Integer,
        db.ForeignKey('tbl_proximity.id')  # ForeignKey to tbl_proximity.id
    )

    # Optional: relationships
    planx = db.relationship('AdvertiserPlanx', backref='proximity_mappings', lazy=True)
    proximity = db.relationship('Proximity', backref='planx_mappings', lazy=True)
