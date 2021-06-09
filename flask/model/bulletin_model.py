from .db_base import db


class Bulletin(db.Model):
    __tablename__ = 'bulletin'

    seq = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100, 'utf8mb4_unicode_ci'), nullable=True)
    content = db.Column(db.String(200, 'utf8mb4_unicode_ci'), nullable=True)
    created = db.Column(db.DateTime)
    created_by_id = db.Column(db.ForeignKey('user.id', onupdate='CASCADE'), index=True)

    created_by = db.relationship('User', primaryjoin='Bulletin.created_by_id == User.id', backref='bulletins')

    def __repr__(self):
        return f'<Bulletin {self.seq} | {self.title} | {self.created_by}>'

    def to_dict(self):
        return dict(
            seq=self.seq,
            title=self.title,
            content=self.content,
            created=self.created,
            created_by=self.created_by
        )
