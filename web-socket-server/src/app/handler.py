from .config import app


@app.route('/healthz')
def hello():
    return 'healthz'
