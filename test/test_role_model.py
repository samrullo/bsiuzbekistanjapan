import unittest
from application.auth.models import Role, Permissions
from application import create_app, db
from base_test_class import BaseTestCase


class RoleModelTest(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        Role.insert_roles()

    def test_has_permission(self):
        role = Role.query.filter_by(name="User").first()
        self.assertTrue(role.has_permission(Permissions.VIEW_USER_INFO))
        self.assertTrue(role.has_permission(Permissions.ADD_WEIGHT))

    def test_add_permission(self):
        role = Role(name="SOMENEWROLE")
        role.add_permission(Permissions.ADD_BSI_WEIGHT)
        self.assertTrue(role.has_permission(Permissions.ADD_BSI_WEIGHT))
        self.assertFalse(role.has_permission(Permissions.ADMIN))

    def test_remove_permissions(self):
        role = Role.query.filter_by(name="Administrator").first()
        role.remove_permission(Permissions.ADMIN)
        self.assertFalse(role.has_permission(Permissions.ADMIN))
        self.assertTrue(role.has_permission(Permissions.ADD_BSI_WEIGHT))

    def test_reset_permissions(self):
        role = Role.query.filter_by(name="Moderator").first()
        role.reset_permissions()
        self.assertTrue(role.permissions == 0)
        self.assertFalse(role.has_permission(Permissions.ADD_BSI_WEIGHT))
