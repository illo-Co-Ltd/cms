# coding: utf-8
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = (
        db.UniqueConstraint('userid', name='user_userid_uindex'),
        {'mysql_collate': 'utf8mb4_unicode_ci'}
    )

    _id = db.Column(db.INTEGER, primary_key=True, nullable=False, autoincrement=True)
    userid = db.Column(db.VARCHAR(16), nullable=False)
    password = db.Column(db.VARCHAR(16), nullable=False)
    username = db.Column(db.VARCHAR(16), nullable=False)
    company = db.Column(db.VARCHAR(16), nullable=False)
    created = db.Column(db.TIMESTAMP)
    created_by = db.Column(db.INTEGER)
    last_edited = db.Column(db.TIMESTAMP)
    edited_by = db.Column(db.INTEGER)
    is_admin = db.Column(db.BOOLEAN)
    is_deleted = db.Column(db.BOOLEAN)

    def has_password(self):
        self.userpwd = generate_password_hash(self.userpwd).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.userpwd, password)

    def to_dict(self):
        return dict(_id=self._id,
                    userid=self.userid,
                    password=self.password,
                    username=self.username,
                    company=self.company,
                    created=self.created,
                    last_edited=self.last_edited,
                    edited_by=self.edited_by,
                    is_admin=self.is_admin,
                    is_deleted=self.is_deleted)