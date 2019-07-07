import models
from app import db
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,\
                                jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)


class ClientController:
    @staticmethod
    def store():
        try:
            name = request.json['name']
            username = request.json['username']
            email = request.json['email']
            password = request.json['password']

            new_client = models.Client(name, username, email, password)
            db.session.add(new_client)
            db.session.commit()

            return jsonify({'client_id': new_client.id})
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'error': e.orig.args[0]}), 400
        except KeyError as e:
            db.session.rollback()
            return jsonify({'error': 'Missing ' + ','.join(e.args)}), 400

    @staticmethod
    def login():
        try:
            username = request.json['username']
            password = request.json['password']

            client = models.Client.query.filter_by(username=username).first()
            if client:
                if client.check_password(password):
                    return jsonify({
                        'access_token': create_access_token(identity=username)
                    })

            return jsonify({'error': 'Unauthorized'}), 401

        except KeyError as e:
            return jsonify({'error': 'Missing ' + ','.join(e.args)}), 400

    @staticmethod
    def get():
        current_client = get_jwt_identity()
        client = models.Client.query.filter_by(username=current_client).first()
        if not client:
            return jsonify({'error': 'There is no client.'}), 404
        return jsonify(client.serialize())

    @staticmethod
    def put():
        try:
            client_id = request.json['id']
            new_password = request.json['password']

            client = models.Client.query.filter_by(id=client_id).first()

            client.set_password(new_password)

            db.session.add(client)
            db.session.commit()

            return jsonify('Client password updated')
        except KeyError as e:
            db.session.rollback()
            return jsonify({'error': 'Missing ' + ','.join(e.args)}), 400


class Token:
    @staticmethod
    def logout():
        jti = get_raw_jwt()['jti']

        token_revoked = models.TokenRevoked()
        token_revoked.jti = jti
        db.session.add(token_revoked)
        db.session.commit()

        return jsonify({"msg": "Successfully logged out"}), 200


class ProjectsController:
    @staticmethod
    def store():
        try:
            title = request.json['title']
            client_id = request.json['client_id']

            new_project = models.Project(title, client_id)
            db.session.add(new_project)
            db.session.commit()

            return jsonify({'project': new_project.id})
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'error': e.orig.args[0]}), 400
        except KeyError as e:
            db.session.rollback()
            return jsonify({'error': 'Missing ' + ','.join(e.args)}), 400

    @staticmethod
    def list():
        current_client = models.Client.query.filter_by(username=get_jwt_identity()).first()
        projects = models.Project.query.filter_by(client_id=current_client.id).all()

        projects_list = []

        for project in projects:
            projects_list.append(project.serialize())

        return jsonify(projects_list)

    @staticmethod
    def get(project_id):
        current_client = models.Client.query.filter_by(username=get_jwt_identity()).first()
        project = models.Project.query.filter_by(client_id=current_client.id, id=project_id).first()

        if project is None:
            return jsonify({'error': 'There is no project with this ID for this user'}), 404

        return jsonify(project.serialize())
