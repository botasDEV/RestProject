from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Set the Flask app
app = Flask(__name__)

# Set the app Configs
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/app.db'
app.config['ENVIRONMENT'] = False

# Initialize dependencies
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Create a folder for the database
if not os.path.exists("database"):
    os.mkdir("database")

# Import dependencies usage classes
import models


if __name__ == '__main__':
    app.run(debug=True)
