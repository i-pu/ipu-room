from .config import db


class User(db.Model):
    __tablename__ = 'users'

    # id is socket_id
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    room_id = db.Column(db.String(36), db.ForeignKey('rooms.id'), nullable=True)

    room = db.relationship('Room', back_populates='members')
    comments = db.relationship('Comment', back_populates='user', cascade='save-update')

    def __repr__(self):
        return 'User(id: {}, name: {}, room_id: {})' \
            .format(self.id, self.name, self.room_id)

    def __to_dict__(self):
        return {
            'id': self.id,
            'name': self.name,
            'room_id': self.room_id,
        }
