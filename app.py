from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_refresh_token_required, create_access_token
import os


# Set the Flask app
app = Flask(__name__)
api = Api(app)

# Set the app Configs
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False


# Create a folder for the database
if not os.path.exists("database"):
    os.mkdir("database")


# Initialize dependencies
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# Initialize DB
import models

from routes import add_routes
add_routes(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(token):
    return db.session.query(db.exists().where(models.TokenRevoked.jti == token['jti'])).scalar()


if __name__ == '__main__':
    app.run(port=80)
