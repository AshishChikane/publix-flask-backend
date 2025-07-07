from Config.db import db

class Currency(db.Model):
    __tablename__ = 'currency'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    code = db.Column(db.String(255))
    symbol = db.Column(db.String(255))

    # No timestamps or relationships specified
