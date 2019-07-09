import os

from app import create_app

env = os.getenv('IPU_ENV')
port = os.getenv('PORT')
webapp, socketio = create_app(env)

if env == 'dev':
    socketio.run(webapp, debug=True, port=int(port), host='0.0.0.0')
else:
    socketio.run(webapp, debug=False, port=int(port), host='0.0.0.0')
