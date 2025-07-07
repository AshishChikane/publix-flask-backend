from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/python_demo'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mypassword@localhost/python_demo'

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:-0SBPNl7(NB%::KI@34.93.210.211/publiX"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return db
