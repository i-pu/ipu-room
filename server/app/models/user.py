from .config import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=True)

    def __init__(self, name, room_id=None):
        self.name = name
        self.room_id = room_id

    def __repr__(self):
        return 'id: {}, name: {}, room_id: {}'.format(self.id, self.name, self.room_id)
