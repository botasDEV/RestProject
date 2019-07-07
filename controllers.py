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

    @staticmethod
    def put(project_id):
        try:
            title = request.json['title']

            current_client = models.Client.query.filter_by(username=get_jwt_identity()).first()
            project = models.Project.query.filter_by(client_id=current_client.id, id=project_id).first()

            if project is None:
                return jsonify({'error': 'You don\'t have permissions to do this.'}), 401

            project.title = title
            db.session.add(project)
            db.session.commit()

            return jsonify(project.serialize())
        except KeyError as e:
            db.session.rollback()
            return jsonify({'error': 'Missing ' + ','.join(e.args)}), 400

    @staticmethod
    def delete(project_id):
        current_client = models.Client.query.filter_by(username=get_jwt_identity()).first()
        project = models.Project.query.filter_by(client_id=current_client.id, id=project_id).first()

        if project is None:
            return jsonify({'error': 'You don\'t have permissions to do this.'}), 401

        db.session.delete(project)
        db.session.commit()

        return jsonify('Project removed successfully')


class TasksController:
    @staticmethod
    def store(project_id):
        try:
            current_client = models.Client.query.filter_by(username=get_jwt_identity()).first()
            project = models.Project.query.filter_by(client_id=current_client.id, id=project_id).first()

            if project is None:
                return jsonify({'error': 'You don\'t have permissions to do this.'}), 401

            title = request.json['title']

            new_task = models.Task(title, project_id)
            db.session.add(new_task)
            db.session.commit()

            return jsonify({'task': new_task.id})
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'error': e.orig.args[0]}), 400
        except KeyError as e:
            db.session.rollback()
            return jsonify({'error': 'Missing ' + ','.join(e.args)}), 400

    @staticmethod
    def list(project_id):
        current_client = models.Client.query.filter_by(username=get_jwt_identity()).first()
        project = models.Project.query.filter_by(client_id=current_client.id, id=project_id).first()

        if project is None:
            return jsonify({'error': 'You don\'t have permissions to do this.'}), 401

        tasks = models.Task.query.filter_by(project_id=project.id).all()

        tasks_list = []
        for task in tasks:
            tasks_list.append(task.serialize())

        return jsonify(tasks_list)

    @staticmethod
    def get(project_id, task_id):
        current_client = models.Client.query.filter_by(username=get_jwt_identity()).first()
        project = models.Project.query.filter_by(client_id=current_client.id, id=project_id).first()

        if project is None:
            return jsonify({'error': 'You don\'t have permissions to do this.'}), 401

        task = models.Task.query.filter_by(project_id=project.id, id=task_id).first()

        if task is None:
            return jsonify({'error': 'There is no task with this ID for this project'}), 404

        return jsonify(task.serialize())

    @staticmethod
    def put(project_id, task_id):
        try:
            title = request.json['title']
            order = request.json['order']
            completed = request.json['completed']

            current_client = models.Client.query.filter_by(username=get_jwt_identity()).first()
            project = models.Project.query.filter_by(client_id=current_client.id, id=project_id).first()

            if project is None:
                return jsonify({'error': 'You don\'t have permissions to do this.'}), 401

            task = models.Task.query.filter_by(project_id=project.id, id=task_id).first()

            if task is None:
                return jsonify({'error': 'There is no task with this ID for this project'}), 404

            if task.completed:
                return jsonify({'error': 'This task is closed so it is not possible to change it anymore.'}), 401

            task.title = title
            task.order = order
            task.completed = completed

            db.session.add(task)
            db.session.commit()

            return jsonify(task.serialize())
        except KeyError as e:
            db.session.rollback()
            return jsonify({'error': 'Missing ' + ','.join(e.args)}), 400

    @staticmethod
    def delete(project_id, task_id):
        current_client = models.Client.query.filter_by(username=get_jwt_identity()).first()
        project = models.Project.query.filter_by(client_id=current_client.id, id=project_id).first()

        if project is None:
            return jsonify({'error': 'You don\'t have permissions to do this.'}), 401

        task = models.Task.query.filter_by(project_id=project.id, id=task_id).first()

        if task is None:
            return jsonify({'error': 'There is no task with this ID for this project'}), 404

        if task.completed:
            return jsonify({'error': 'This task cannot be deleted since it is complete.'}), 401

        db.session.delete(task)
        db.session.commit()

        return jsonify('Task removed successfully')