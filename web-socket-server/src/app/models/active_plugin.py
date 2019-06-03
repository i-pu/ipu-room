from .config import db, uuid4_for_str


class ActivePlugin(db.Model):
    __tablename__ = 'active_plugins'

    id = db.Column(db.String(36), primary_key=True, default=uuid4_for_str)
    room_id = db.Column(db.String(36), db.ForeignKey('rooms.id'))
    plugin_id = db.Column(db.String(36), db.ForeignKey('plugins.id'))
    enabled = db.Column(db.Boolean, default=True)

    room = db.relationship('Room', back_populates='active_plugins', cascade='all')

    def __repr__(self):
        return 'ActivePlugin(id: {}, room_id: {}, plugin_id: {})' \
            .format(self.id, self.room_id, self.plugin_id)

    def __to_dict__(self):
        return {
            'id': self.id,
            'room_id': self.room_id,
            'plugin_id': self.plugin_id
        }
