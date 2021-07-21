import os
from flask import Flask, render_template

from . import db


def create_app(test_config=None):
    app = Flask("todo", instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'todo.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import auth
    app.register_blueprint(auth.bp)

    from . import db
    db.init_app(app) 

    from . import todo
    app.register_blueprint(todo.bp)

    @app.route("/")
    def welcome():
        return render_template("welcome.html")

    return app

