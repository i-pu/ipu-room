from .config import db, uuid4_for_str


class ActivePlugin(db.Model):
    __tablename__ = 'active_plugins'

    id = db.Column(db.String(36), primary_key=True, default=uuid4_for_str)
    room_id = db.Column(db.String(36), db.ForeignKey('rooms.id'))
    plugin_id = db.Column(db.String(36), db.ForeignKey('plugins.id'))
