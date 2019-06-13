from app import create_app
import os

env = os.getenv('IPU_ENV')
port = os.getenv('PORT')
app, socketio = create_app(env)

if __name__ == '__main__':
    if env == 'dev':
        socketio.run(app, debug=True, port=int(port), host='0.0.0.0')
    else:
        socketio.run(app, debug=False, port=int(port), host='0.0.0.0')
