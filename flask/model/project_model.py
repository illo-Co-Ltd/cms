from .db_base import db, env


class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    if env == 'development':
        name = db.Column(db.String(20, 'utf8mb4_unicode_ci'), unique=True)
        shorthand = db.Column(db.String(5, 'utf8mb4_unicode_ci'), unique=True)
    else:
        name = db.Column(db.String(20, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
        shorthand = db.Column(db.String(5, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    description = db.Column(db.String(200, 'utf8mb4_unicode_ci'))
    created = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    started = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    ended = db.Column(db.TIMESTAMP(timezone=True))
    created_by_id = db.Column(db.ForeignKey('user.id', onupdate='CASCADE'), index=True)

    created_by = db.relationship('User', primaryjoin='Project.created_by_id == User.id',
                                 backref='projects')

    def __repr__(self):
        return f'<Project {self.name} | {self.shorthand}>'

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            shorthand=self.shorthand,
            description=self.description,
            created=self.created,
            started=self.started,
            ended=self.ended,
            created_by=self.created_by,
        )
