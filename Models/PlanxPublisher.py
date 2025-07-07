from Config.db import db

class PlanXPublisher(db.Model):
    __tablename__ = 'tbl_planx_publisher_mapping'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    planx_id = db.Column(
        db.Integer,
        db.ForeignKey('tbl_advertiser_planx.id')  # FK to tbl_advertiser_planx.id
    )
    publisher_id = db.Column(
        db.Integer,
        db.ForeignKey('tbl_publisher.id')  # FK to tbl_publisher.id
    )

    # Optional: relationships
    planx = db.relationship('AdvertiserPlanx', backref='publisher_mappings', lazy=True)
    publisher = db.relationship('Publisher', backref='planx_mappings', lazy=True)
