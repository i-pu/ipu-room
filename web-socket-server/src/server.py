from app import create_app
import os

env = os.getenv('ENV')
port = os.getenv('PORT')
app, socketio = create_app(env)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=int(port), host='0.0.0.0')
