import unittest

from blog.models.user import User, Permission, Role


class UserModelTestCase(unittest.TestCase):
    Role.init_roles()

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='dog')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_user_role(self):
        u = User(username='Arrackisarookie', password='you guess')
        self.assertTrue(u.can(Permission.LIKE))
        self.assertTrue(u.can(Permission.LEAVEMSG))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertTrue(u.can(Permission.MODERATE))
        self.assertTrue(u.can(Permission.ADMIN))

    # def test_anonymous_user(self):
    #     u = AnonymousUser()
    #     self.assertFalse(u.can(Permission.LIKE))
    #     self.assertFalse(u.can(Permission.LEAVEMSG))
    #     self.assertFalse(u.can(Permission.WRITE))
    #     self.assertFalse(u.can(Permission.MODERATE))
    #     self.assertFalse(u.can(Permission.ADMIN))
