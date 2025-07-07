from Config.db import db

class DaywiseFootfall(db.Model):
    __tablename__ = 'tbl_daywise_footfall'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    day_name = db.Column(db.String(255))
    day_short = db.Column(db.String(255))
    percent = db.Column(db.Float)  # DOUBLE → Float
    screen_id = db.Column(
        db.Integer,
        db.ForeignKey('tbl_screens.id')  # references tbl_screens.id
    )

    # Optional: define relationship to Screen model if you have it
    screen = db.relationship('Screen', backref='daywise_footfalls', lazy=True)
