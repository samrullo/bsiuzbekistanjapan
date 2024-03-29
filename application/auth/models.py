from application import db
from flask_login import UserMixin, AnonymousUserMixin, current_user
from flask import abort
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from application import login_manager
import datetime
from .permissions import Permissions
from functools import wraps
from application.post_weight.models import PostWeight, UserPostWeightPrice
from application.post_weight.models import RepresentedIndividual
from application.post_weight.models import Recipient


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(250))
    username = db.Column(db.String(200))
    phone = db.Column(db.String(64), nullable=True)
    telegram_username = db.Column(db.String(250), nullable=True)
    address = db.Column(db.String(250), nullable=True)
    password_hash = db.Column(db.String(128))
    registered_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_confirmed = db.Column(db.Boolean)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_google_account = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    post_weights = db.relationship("PostWeight", backref="user", lazy="dynamic")
    represented_individuals = db.relationship("RepresentedIndividual", backref="user", lazy="dynamic")
    recipients = db.relationship("Recipient", backref="user", lazy="dynamic")
    user_post_weight_prices = db.relationship("UserPostWeightPrice", backref="user", lazy="dynamic")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email == current_app.config.get("ADMIN_EMAIL"):
            self.role = Role.query.filter_by(name="Administrator").first()
        else:
            self.role = Role.query.filter_by(default=True).first()

    def set_username(self):
        USERNAME_CHAR_COUNT = 8
        name_tokens = self.name.split(" ")
        if len(name_tokens) > 1:
            last_name = name_tokens[0]
            first_name = name_tokens[1]
            if len(last_name) > 7:
                last_name = last_name[:7]
                username = first_name[0] + last_name
            else:
                chars_to_add = USERNAME_CHAR_COUNT - len(last_name)
                username = first_name[:min(chars_to_add, len(first_name))] + last_name
            existing_users = User.query.filter_by(username=username).all()
            if len(existing_users) > 0:
                username = f"{username}{len(existing_users)}"
            self.username = username.lower()
            db.session.add(self)
            db.session.commit()

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

    def is_moderator(self):
        return self.can(Permissions.ADD_BSI_WEIGHT)

    def update_last_seen(self):
        self.last_seen = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

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
        roles = {"User": [Permissions.VIEW_USER_INFO, Permissions.ADD_WEIGHT],
                 "Moderator": [Permissions.VIEW_USER_INFO, Permissions.ADD_WEIGHT, Permissions.ADD_BSI_WEIGHT],
                 "Administrator": [Permissions.VIEW_USER_INFO,
                                   Permissions.ADD_WEIGHT, Permissions.ADD_BSI_WEIGHT, Permissions.ADMIN], }
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
