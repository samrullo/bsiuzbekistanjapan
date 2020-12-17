from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import current_app


class UserModelView(ModelView):
    column_exclude_list = ['password_hash', 'registered_on', 'confirmed_on', 'is_confirmed', 'post_weights',
                           'is_google_account', 'role_id', 'last_seen']
    column_editable_list = ['email', 'name', 'phone', 'address', 'is_confirmed']
    form_excluded_columns = ['password_hash', 'registered_on', 'confirmed_on', 'post_weights', 'is_google_account',
                             'last_seen']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_confirmed and current_user.is_administrator()


class RoleModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_confirmed and current_user.is_administrator()


class CountryModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_confirmed and current_user.is_administrator()


class RepresentedIndividualView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_confirmed and current_user.is_administrator()


class RecipientView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_confirmed and current_user.is_administrator()


class PostWeightView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_confirmed and current_user.is_administrator()


class PostWeightContentView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_confirmed and current_user.is_administrator()


class UserPostWeightPriceView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_confirmed and current_user.is_administrator()


class BSIPostWeightView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_confirmed and current_user.is_administrator()
