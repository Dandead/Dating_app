from django.utils import timezone
from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from users.models import DatingUserNickname, DatingProfile


class TestDatingUserModel(TestCase):

    user = get_user_model()

    def test_user_create(self):
        self.user_instance = self.user.objects.create_user(
            email="test@test.com", password="test"
        )
        self.assertEqual(self.user_instance.email, "test@test.com")
        self.assertEqual(self.user.objects.count(), 1)
        self.assertTrue(self.user_instance.is_active)
        self.assertFalse(self.user_instance.is_staff)
        self.assertFalse(self.user_instance.is_superuser)
        self.assertEqual(str(self.user_instance), self.user_instance.email)

    def test_user_empty_email(self):
        with self.assertRaises(ValueError):
            self.user_instance = self.user.objects.create_user(
                email="", password="test"
            )

    def test_user_none_email(self):
        with self.assertRaises(ValueError):
            self.user_instance = self.user.objects.create_user(
                email=None, password="test"
            )

    def test_user_unique_email(self):
        self.user.objects.create_user(email="test@test.com", password="test")
        with self.assertRaises(IntegrityError):
            self.user.objects.create_user(email="test@test.com", password="test")

    def test_user_string(self):
        self.user_instance = self.user.objects.create_user(
            email="test@test.com", password="test"
        )
        self.assertEqual(str(self.user_instance), "test@test.com")


class TestDatingUserNicknameModel(TestCase):

    user = get_user_model()

    def test_nickname_create(self):
        self.user_instance = self.user.objects.create_user(
            email="test@test.com", password="test"
        )
        self.nickname = DatingUserNickname.objects.create(
            user=self.user_instance, nickname="test"
        )
        self.assertEqual(self.user.objects.count(), 1)
        self.assertEqual(self.user_instance.nick.nickname, "test")
        self.assertEqual(self.nickname.nickname, "test")
        self.assertEqual(self.user_instance, self.nickname.user)

    def test_nickname_unique(self):
        self.first_user = self.user.objects.create_user(
            email="test1@test.com", password="test"
        )
        self.second_user = self.user.objects.create_user(
            email="test2@test.com", password="test"
        )
        DatingUserNickname.objects.create(user=self.first_user, nickname="test")
        with self.assertRaises(IntegrityError):
            DatingUserNickname.objects.create(user=self.second_user, nickname="test")

    def test_nickname_one_to_one(self):
        self.user_instance = self.user.objects.create_user(
            email="test@test.com", password="test"
        )
        DatingUserNickname.objects.create(user=self.user_instance, nickname="test1")
        with self.assertRaises(IntegrityError):
            DatingUserNickname.objects.create(user=self.user_instance, nickname="test2")


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
