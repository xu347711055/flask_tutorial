import os
from flask import Flask, jsonify
from .models import *


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.logger.debug('creating app...')
    app.logger.debug('param __name__ is %s' % __name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )
    app.logger.debug(app.instance_path)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/insert")
    def add_user():
        u = User('aaasa', 'aasaa')
        db_session.add(u)
        db_session.commit()
        users = db_session.query(User).all()
        print(users)
        # users = User.query.all()

        return jsonify(users)

    # @app.route("/get")
    # def get_user():
    #     users = User.query.all()
    #     return jsonify(users)


    # from . import db
    # db.init_app(app)
    # app.logger.debug('Created app flaskr.')

    from . import database
    database.init_db()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        database.db_session.remove()

    from .import auth
    app.register_blueprint(auth.bp)
    from .import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app


