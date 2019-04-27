from app import create_app
import os

if __name__ == '__main__':
    env = os.getenv('ENV')
    app, socketio = create_app(env)
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)
