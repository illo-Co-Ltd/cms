from sqlalchemy import UniqueConstraint

from .db_base import db, env


class DeviceEntry(db.Model):
    __tablename__ = 'device_entry'
    __table_args__ = (
        # TODO
        # table 옵션 찾아보기
        # 'autoload':True,
        UniqueConstraint('device_id', 'project_id'), {}
        # 'mysql_collate': 'utf8mb4_unicode_ci'
    )

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.ForeignKey('device.id', onupdate='CASCADE'), nullable=False, index=True)
    project_id = db.Column(db.ForeignKey('project.id', onupdate='CASCADE'), nullable=False, index=True)
    created = db.Column(db.DateTime)
    created_by_id = db.Column(db.ForeignKey('user.id', onupdate='CASCADE'), index=True)

    device = db.relationship('Device', primaryjoin='DeviceEntry.device_id == Device.id',
                             backref='device_entries')
    project = db.relationship('Project', primaryjoin='DeviceEntry.project_id == Project.id',
                              backref='device_entries')
    created_by = db.relationship('User', primaryjoin='DeviceEntry.created_by_id == User.id',
                                 backref='device_entries')

    def __repr__(self):
        return f'<DeviceEntry [{self.device}] | [{self.project}]>'

    def to_dict(self):
        return dict(
            id=self.id,
            device=self.device,
            project=self.project,
            created=self.created,
            created_by=self.created_by,
        )
