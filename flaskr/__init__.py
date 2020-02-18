import os
from config import app_config
from flask import Flask


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(app_config[app.config['ENV']])

    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from flaskr import db
    db.init_app(app)

    from flaskr import auth
    app.register_blueprint(auth.bp)

    from flaskr import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    from flaskr import plot
    app.register_blueprint(plot.bp)

    return app


# actually: https://flask.palletsprojects.com/en/1.1.x/tutorial/views/