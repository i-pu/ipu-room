from .config import db, uuid4_for_str


class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.String(36), primary_key=True, default=uuid4_for_str)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime)
    thumbnail_url = db.Column(db.String(255), nullable=True)

    users = db.relationship("User", back_populates="room", cascade='save-update')
    comments = db.relationship("Comment", back_populates="room", cascade='save-update, delete, delete-orphan')

    def __repr__(self):
        return 'id: {}, name: {}, created_at: {}, thumbnail_url: {}, users: {}'. \
            format(self.id, self.name, self.created_at, self.thumbnail_url, self.users)

    def __to_dict__(self):
        return {
            'room': {
                'id': self.id,
                'name': self.name,
                'created_at': self.created_at,
                'thumbnail_url': self.thumbnail_url,
                'users': self.users,
                'comments': self.comments
            }
        }
