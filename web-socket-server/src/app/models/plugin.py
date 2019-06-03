from .config import db, uuid4_for_str


class Plugin(db.Model):
    __tablename__ = 'plugins'

    id = db.Column(db.String(255), primary_key=True, default=uuid4_for_str)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    version = db.Column(db.String(255))
    thumbnail_url = db.Column(db.String(255))
    author = db.Column(db.String(255))
    tags = db.Column(db.String(255))
    requirements = db.Column(db.String(255))
    last_updated = db.Column(db.String(255))
    published = db.Column(db.Boolean)
    python = db.Column(db.Text)
    template = db.Column(db.Text)

    def __repr__(self):
        return 'Plugin(id: {}, name: {}, description: {})' \
            .format(self.id, self.name, self.description)

    def __to_dict__(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'version': self.version,
            'thumbnail_url': self.thumbnail_url,
            'author': self.author,
            'tags': self.tags,
            'requirements': self.requirements,
            'last_updated': self.last_updated,
            'published': self.published,
            'python': self.python,
            'template': self.template,
        }
