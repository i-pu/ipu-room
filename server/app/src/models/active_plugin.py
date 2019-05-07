from .config import db, uuid4_for_str


class ActivePlugin(db.Model):
    __tablename__ = 'active_plugins'

    id = db.Column(db.String(36), primary_key=True, default=uuid4_for_str)
    room_id = db.Column(db.String(36), db.ForeignKey('rooms.id'))
    name = db.Column(db.String(36), db.ForeignKey('plugins.name'))

    room = db.relationship('Room', back_populates='active_plugins', cascade='all')

    def __repr__(self):
        return 'id: {}, room_id: {}, name: {}' \
            .format(self.id, self.room_id, self.name)
