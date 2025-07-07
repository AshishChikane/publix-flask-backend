from Config.db import db

class UserType(db.Model):
    __tablename__ = 'tbl_users_type'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_type = db.Column(db.String(255))  # You can adjust length as needed

    # Relationships (if needed) can be added here
