from extensions import db

class AuthPermissions(db.Model):
    __tablename__ = "auth_permission"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)
    content_type_id = db.Column(db.Integer)
    codename = db.Column(db.String(80), unique=True)
    microservice_id = db.Column(db.Integer, db.ForeignKey('microservices.id'))
    microservice = db.relationship("Microservices")


    @property
    def list(self):
        return {
            "name": self.name,
            "content_type_id": self.content_type_id,
            "codename": self.codename,
            "microservice": self.microservice.codename if hasattr(self.microservice, 'codename') else False
        }


class AuthGroups(db.Model):
    __tablename__="auth_group"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)
    created_on = db.Column(db.String(100))
    auth_group_permissions=db.relationship('AuthGroupPermissions', backref='authgroupperm', lazy='dynamic')

    @property
    def list(self):
        return {
            "id": self.id,
            "name": self.name
        }


class AuthGroupPermissions(db.Model):
    __tablename__="auth_group_permissions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, db.ForeignKey('auth_group.id'))
    permission_id = db.Column(db.Integer, db.ForeignKey('auth_permission.id'))
    created_on = db.Column(db.String(100))
    #auth_permissions=db.relationship('AuthPermissions', backref='authpermits', lazy='dynamic')

    @property
    def list(self):
        return {
            "id": self.id,
            "group_id": self.group_id
        }


class Microservices(db.Model):
    __tablename__ = "microservices"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    codename = db.Column(db.String(80), unique=True)

    @property
    def list(self):
        return {
            "id": self.id,
            "name": self.name,
            "codename": self.codename
        }
