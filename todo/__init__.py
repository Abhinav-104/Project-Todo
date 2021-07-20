import os
from flask import Flask, render_template







def create_app():
    app = FLask("todo", instance_relative_config=True)
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

    @app.route("/")
    def welcome():


    return app

