from flask_bcrypt import generate_password_hash, check_password_hash
from .db_base import db, env


# noinspection PyAttributeOutsideInit
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    if env == 'development':
        userid = db.Column(db.String(16, 'utf8mb4_unicode_ci'), unique=True)
        password = db.Column(db.String(60, 'utf8mb4_unicode_ci'))
        username = db.Column(db.String(16, 'utf8mb4_unicode_ci'))
        company_id = db.Column(db.ForeignKey('company.id', onupdate='CASCADE'), index=True)
    else:
        userid = db.Column(db.String(16, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
        password = db.Column(db.String(60, 'utf8mb4_unicode_ci'), nullable=False)
        username = db.Column(db.String(16, 'utf8mb4_unicode_ci'), nullable=False)
        company_id = db.Column(db.ForeignKey('company.id', onupdate='CASCADE'), nullable=False, index=True)
    created = db.Column(db.DateTime)
    last_edited = db.Column(db.DateTime)
    is_admin = db.Column(db.Integer)
    is_deleted = db.Column(db.Integer)

    company = db.relationship('Company', primaryjoin='User.company_id == Company.id', backref='user_company_company_id',
                              uselist=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return dict(
            id=self.id,
            userid=self.userid,
            password=self.password,
            username=self.username,
            company=self.company,
            created=self.created,
            last_edited=self.last_edited,
            edited_by=self.edited_by,
            is_admin=self.is_admin,
            is_deleted=self.is_deleted
        )
