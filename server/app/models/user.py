from .config import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    room_id = db.Column(db.String(255), db.ForeignKey('rooms.id'), nullable=True)
    socket_id = db.Column(db.String(255), nullable=True)
