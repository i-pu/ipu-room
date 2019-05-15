from .config import db, uuid4_for_str
from .user import User
from .active_plugin import ActivePlugin


class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.String(36), primary_key=True, default=uuid4_for_str)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime)
    thumbnail_url = db.Column(db.String(255), nullable=True)

    members = db.relationship("User", back_populates="room", cascade='save-update')
    comments = db.relationship("Comment", back_populates="room", cascade='save-update, delete, delete-orphan')
    active_plugins = db.relationship("ActivePlugin", back_populates="room", cascade='all')

    def __repr__(self):
        return 'Room(id: {}, name: {}, created_at: {}, thumbnail_url: {}, members: {}, active_plugins: {})' \
            .format(self.id, self.name, self.created_at, self.thumbnail_url, self.members, self.active_plugins)

    def __to_dict__(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'thumbnail_url': self.thumbnail_url,
            'members': list(map(User.__to_dict__, self.members)),
            'comments': self.comments,
            'plugins': list({'config': map(ActivePlugin.__to_dict__, self.active_plugins)}),
        }
