from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import os


# Set the Flask app
app = Flask(__name__)
api = Api(app)
# Set the app Configs
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a folder for the database
if not os.path.exists("database"):
    os.mkdir("database")


# Initialize dependencies
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Initialize DB
import schemas
db.create_all()

from routes import add_routes
add_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
