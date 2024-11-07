from django.test import TestCase
from django.contrib.auth import get_user_model


class CreateDatingUserTests(TestCase):
    """Test module for creating a new dating user"""

    def test_create_user(self):
        user_model = get_user_model()
        user = user_model.objects.create_user(
            email="simpleuser@user.com", password="foo12345"
        )
        self.assertEqual(user.email, "simpleuser@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(TypeError):
            user_model.objects.create_user()
        with self.assertRaises(TypeError):
            user_model.objects.create_user(email="")
        with self.assertRaises(ValueError):
            user_model.objects.create_user(email="", password="foo12345")

    def test_create_superuser(self):
        user_model = get_user_model()
        admin_user = user_model.objects.create_superuser(
            email="admin@admin.com",
            password="foo12345",
        )
        self.assertEqual(admin_user.email, "admin@admin.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            user_model.objects.create_superuser(
                email="admin@admin.com",
                password="foo12345",
                first_name="User",
                last_name="Name",
                gender="M",
                is_superuser=False,
            )
