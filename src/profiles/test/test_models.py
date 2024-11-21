from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.utils import IntegrityError
from profiles.models import DatingProfile
from users.models import DatingUserNickname


class TestDatingProfile(TestCase):

    user = get_user_model()
    time = timezone.localdate()

    def test_profile_create(self):
        self.user_instance = self.user.objects.create_user(
            email="test@test.com", password="test"
        )
        self.profile = DatingProfile.objects.create(
            user=self.user_instance,
            first_name="test_name",
            last_name="test_surname",
            birthday=self.time,
            gender="M",
        )
        self.assertEqual(DatingProfile.objects.count(), 1)
        self.assertEqual(self.profile.user, self.user_instance)
        self.assertEqual(self.profile.first_name, "test_name")
        self.assertEqual(self.profile.last_name, "test_surname")
        self.assertEqual(self.profile.birthday, self.time)
        self.assertEqual(self.profile.gender, "M")

    def test_profile_none_fields(self):
        self.user_instance = self.user.objects.create_user(
            email="test@test.com", password="test"
        )
        self.profile = DatingProfile.objects.create(
            user=self.user_instance,
            first_name="test_name",
            last_name="test_surname",
            birthday=None,
            gender="M",
        )
        self.assertEqual(DatingProfile.objects.count(), 1)
        self.assertIsNone(self.profile.birthday)

    def test_profile_one_to_one(self):
        self.user_instance = self.user.objects.create_user(
            email="test@test.com", password="test"
        )
        self.profile = DatingProfile.objects.create(
            user=self.user_instance,
            first_name="test_name",
            last_name="test_surname",
            birthday=None,
            gender="M",
        )
        with self.assertRaises(IntegrityError):
            DatingProfile.objects.create(
                user=self.user_instance,
                first_name="test2_name",
                last_name="test2_surname",
                birthday=None,
                gender="F",
            )

    def test_profile_string(self):
        self.user_instance = self.user.objects.create_user(
            email="test@test.com", password="test"
        )
        self.profile = DatingProfile.objects.create(
            user=self.user_instance,
            first_name="test_name",
            last_name="test_surname",
            birthday=None,
            gender="M",
        )
        self.assertEqual(str(self.profile), "test@test.com's profile")
