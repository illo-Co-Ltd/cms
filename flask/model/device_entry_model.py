from .db_base import db, env


class DeviceEntry(db.Model):
    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.ForeignKey('device.id', onupdate='CASCADE'), nullable=False, index=True)
    project = db.Column(db.ForeignKey('project.id', onupdate='CASCADE'), nullable=False, index=True)
    created = db.Column(db.DateTime)
    created_by = db.Column(db.ForeignKey('user.id', onupdate='CASCADE'), index=True)

    r_device = db.relationship('Device', primaryjoin='DeviceEntry.device == Device.id',
                               backref='device_id_device_entry_device')
    r_project = db.relationship('Project', primaryjoin='DeviceEntry.project == Project.id',
                                backref='project_id_device_entry_project')
    r_created_by = db.relationship('User', primaryjoin='Device.created_by == User.id',
                                   backref='user_id_device_create_by')

    def __repr__(self):
        return f'<DeviceEntry device[{self.device}] | proj[{self.project}]>'

    def to_dict(self):
        return dict(
            id=self.id,
            device=self.device,
            project=self.project,
            created=self.created,
            created_by=self.created_by,
        )
