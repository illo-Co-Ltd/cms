from .db_base import db


class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    subscription = db.Column(db.Integer)
    expiration_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Company {self.name} | {self.expiration_date}>'

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            subscription=self.subscription,
            expiration_date=self.expiration_date
        )