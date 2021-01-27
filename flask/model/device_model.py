from .db_base import db, env


class Device(db.Model):
    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True)
    if env == 'development':
        model = db.Column(db.String(16, 'utf8mb4_unicode_ci'))
        serial = db.Column(db.String(20, 'utf8mb4_unicode_ci'))
        company = db.Column(db.ForeignKey('company.id', onupdate='CASCADE'), index=True)
        owner = db.Column(db.ForeignKey('user.id', onupdate='CASCADE'), index=True)
        ip = db.Column(db.String(15, 'utf8mb4_unicode_ci'), server_default=db.FetchedValue())
    else:
        model = db.Column(db.String(16, 'utf8mb4_unicode_ci'), nullable=False)
        serial = db.Column(db.String(20, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
        company = db.Column(db.ForeignKey('company.id', onupdate='CASCADE'), nullable=False, index=True)
        owner = db.Column(db.ForeignKey('user.id', onupdate='CASCADE'), nullable=False, index=True)
        ip = db.Column(db.String(15, 'utf8mb4_unicode_ci'), nullable=False, unique=True, server_default=db.FetchedValue())
    created = db.Column(db.DateTime)
    created_by = db.Column(db.ForeignKey('user.id', onupdate='CASCADE'), index=True)
    last_edited = db.Column(db.DateTime)
    edited_by = db.Column(db.ForeignKey('user.id', onupdate='CASCADE'), index=True)
    is_deleted = db.Column(db.Integer)

    r_company = db.relationship('Company', primaryjoin='Device.company == Company.id',
                                backref='company_id_device_company')
    r_created_by = db.relationship('User', primaryjoin='Device.created_by == User.id',
                                   backref='user_id_device_create_by')
    r_edited_by = db.relationship('User', primaryjoin='Device.edited_by == User.id', backref='device_edited_by_user_id')
    r_owner = db.relationship('User', primaryjoin='Device.owner == User.id', backref='device_owner_user_id')

    def __repr__(self):
        return f'<Device {self.model} | {self.serial}>'

    def to_dict(self):
        return dict(
            id=self.id,
            model=self.model,
            serial=self.serial,
            company=self.company,
            owner=self.owner,
            ip=self.ip,
            created=self.created,
            created_by=self.created_by,
            last_edited=self.last_edited,
            edited_by=self.edited_by,
            is_deleted=self.is_deleted
        )
