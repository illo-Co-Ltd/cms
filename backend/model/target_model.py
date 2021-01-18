from .db_base import db


class Target(db.Model):
    __tablename__ = 'target'

    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.ForeignKey('project.id', onupdate='CASCADE'), index=True)
    type = db.Column(db.String(16, 'utf8mb4_unicode_ci'))
    detail = db.Column(db.String(16, 'utf8mb4_unicode_ci'))
    name = db.Column(db.String(16, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    description = db.Column(db.String(200, 'utf8mb4_unicode_ci'))

    r_project = db.relationship('Project', primaryjoin='Target.project == Project.id',
                                backref='target_project_project_id')

    def __repr__(self):
        return f'<Target {self.type} | {self.detail} | {self.name}>'

    def to_dict(self):
        return dict(
            id=self.id,
            type=self.type,
            detail=self.detail,
            name=self.name,
            description=self.description
        )
