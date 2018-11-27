from extensions import db
from passlib.apps import custom_app_context as pwd_context

class User(db.Model):
    __tablename__ = 'auth_user'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(54))
    email = db.Column(db.String(154))
    first_name = db.Column(db.String(54))
    last_name = db.Column(db.String(54))
    is_staff = db.Column(db.Boolean, nullable=False, default=False)
    is_superuser = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    date_joined = db.Column(db.String(154))
    last_login = db.Column(db.String(154))
    user_uuid = db.Column(db.Text)
    auth_user_groups=db.relationship('AuthUserGroups', backref='userauthgrp', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)



class AuthUserGroups(db.Model):
    __tablename__="auth_user_groups"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, db.ForeignKey('auth_group.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'))
    created_on = db.Column(db.String(100))


class Emails(db.Model):
    __tablename__ = 'content_emails'
    id = db.Column(db.Integer, primary_key=True)
    email_message = db.Column(db.Text)
    email_subject = db.Column(db.Text)
    email_name = db.Column(db.Text)
    email_status = db.Column(db.String(26))
    email_slug = db.Column(db.String(26))