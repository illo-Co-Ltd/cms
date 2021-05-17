from flask_bcrypt import generate_password_hash, check_password_hash

from .db_base import db, env


# noinspection PyAttributeOutsideInit
class Device(db.Model):
    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True)
    if env == 'development':
        model = db.Column(db.String(16, 'utf8mb4_unicode_ci'))
        serial = db.Column(db.String(20, 'utf8mb4_unicode_ci'))
        company_id = db.Column(db.ForeignKey('company.id', onupdate='CASCADE'), index=True)
        owner_id = db.Column(db.ForeignKey('user.id', onupdate='CASCADE'), index=True)
        ip = db.Column(db.String(15, 'utf8mb4_unicode_ci'), server_default=db.FetchedValue())
    else:
        model = db.Column(db.String(16, 'utf8mb4_unicode_ci'), nullable=False)
        serial = db.Column(db.String(20, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
        company_id = db.Column(db.ForeignKey('company.id', onupdate='CASCADE'), nullable=False, index=True)
        owner_id = db.Column(db.ForeignKey('user.id', onupdate='CASCADE'), nullable=False, index=True)
        ip = db.Column(db.String(15, 'utf8mb4_unicode_ci'), nullable=False, unique=True,
                       server_default=db.FetchedValue())
    cgi_id= db.Column(db.String(16, 'utf8mb4_unicode_ci'), nullable=False)
    cgi_pw= db.Column(db.String(60, 'utf8mb4_unicode_ci'), nullable=False)
    created = db.Column(db.DateTime)
    created_by_id = db.Column(db.ForeignKey('user.id', onupdate='CASCADE'), index=True)
    last_edited = db.Column(db.DateTime)
    edited_by_id = db.Column(db.ForeignKey('user.id', onupdate='CASCADE'), index=True)
    is_deleted = db.Column(db.Integer)

    company = db.relationship('Company', primaryjoin='Device.company_id == Company.id',
                              backref='devices')
    created_by = db.relationship('User', primaryjoin='Device.created_by_id == User.id',
                                 backref='created_devices')
    edited_by = db.relationship('User', primaryjoin='Device.edited_by_id == User.id', backref='edited_devices')
    owner = db.relationship('User', primaryjoin='Device.owner_id == User.id', backref='owned_devices')

    def __repr__(self):
        return f'<Device {self.model} | {self.serial}>'

    def hash_cgi_pw(self):
        self.password = generate_password_hash(self.cgi_pw).decode('utf8')

    def check_cgi_pw(self, password):
        return check_password_hash(self.cgi_pw, password)

    def to_dict(self):
        return dict(
            id=self.id,
            model=self.model,
            serial=self.serial,
            company=self.company,
            owner=self.owner,
            ip=self.ip,
            cgi_id=self.cgi_id,
            cgi_pw=self.cgi_pw,
            created=self.created,
            created_by=self.created_by,
            last_edited=self.last_edited,
            edited_by=self.edited_by,
            is_deleted=self.is_deleted
        )
