from .config import flask_app


@flask_app.route('/healthz')
def hello():
    return 'healthz'
