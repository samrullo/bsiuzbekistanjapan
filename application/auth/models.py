from application import db
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from application import login_manager
import datetime


class User(UserMixin, db.Model):
    __tablename = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    registered_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_confirmed = db.Column(db.Boolean)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    is_google_account = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email == current_app.config.get("ADMIN_EMAIL"):
            self.role = Role.query.filter_by(name="Administrator").first()
        else:
            self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError("password property is not directly accessible")

    @password.setter
    def password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permissions.ADMIN)

    def __repr__(self):
        return f"<User {self.id}-{self.email} Role id : {self.role_id}>"


class AnonymousUser(AnonymousUserMixin):
    def can(self, perm):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return f"<Role {self.id}-{self.name} Permissions: {self.permissions}>"

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {"User": [Permissions.FOLLOW, Permissions.COMMENT, Permissions.WRITE],
                 "Moderator": [Permissions.FOLLOW, Permissions.COMMENT, Permissions.WRITE, Permissions.MODERATE],
                 "Administrator": [Permissions.FOLLOW, Permissions.COMMENT, Permissions.WRITE, Permissions.MODERATE,
                                   Permissions.ADMIN], }
        for role_name, permissions in roles.items():
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
                if role_name == "User":
                    role.default = True
                role.reset_permissions()
                for perm in permissions:
                    role.add_permission(perm)
                db.session.add(role)
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Permissions:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16
