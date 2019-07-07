import controllers
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,\
                                jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)


def add_routes(app):
    """
    CLIENTS ROUTES
    """
    @app.route('/api/user/login', methods=['POST'])
    def login():
        return controllers.ClientController.login()

    @app.route('/api/user/logout', methods=['DELETE'])
    @jwt_required
    def logout():
        return controllers.Token.logout()

    @app.route('/api/user/register', methods=['POST'])
    def client_post():
        return controllers.ClientController.store()

    @app.route('/api/user', methods=['GET'])
    @jwt_required
    def client_get():
        return controllers.ClientController.get()

    @app.route('/api/user', methods=['PUT'])
    @jwt_required
    def client_put_password():
        return controllers.ClientController.put()

    """
    PROJECTS ROUTES
    """

    @app.route('/api/projects', methods=['POST'])
    @jwt_required
    def create_project():
        return controllers.ProjectsController.store()

    @app.route('/api/projects', methods=['GET'])
    @jwt_required
    def get_projects():
        return controllers.ProjectsController.list()

    @app.route('/api/projects/<project_id>', methods=['GET'])
    @jwt_required
    def get_projects_by_id(project_id):
        return controllers.ProjectsController.get(project_id)


