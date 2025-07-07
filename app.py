# from flask import Flask
# from Config.db import init_db
# from Routes.chatroute import chat_r

# app = Flask(__name__)
# db = init_db(app)

# app.register_blueprint(chat_r)

# if __name__ == '__main__':  # This is the main entry point of the application,It's a standard way to ensure certain code only runs when you execute this file directly
#     with app.app_context(): # Creates a Flask application context,This ensures that the database connection is available when needed ,the with statement ensures the context is properly managed and cleaned up
#         db.create_all()  # Create tables if not exist
#     app.run(debug=True) # Starts the Flask application in debug mode, which provides detailed error messages and automatic reloading when code changes are detected

from flask import Flask
from flask_cors import CORS
from Config.db import init_db
from Routes.chatroute import chat_r

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

db = init_db(app)

app.register_blueprint(chat_r)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
