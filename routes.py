import controllers
from flask import jsonify


def add_routes(app):
    @app.route('/client', methods=['GET'])
    def get_client():
        return jsonify(controllers.ClientController.root())

