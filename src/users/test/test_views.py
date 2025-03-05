from copy import deepcopy

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from users.models import DatingUserNickname, DatingProfile


class UserRegisterAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_create_url = reverse("user-register")
        cls.data = {
            "email": "user@test.com",
            "password": "testpassword05912",
            "nickname": "testuser",
            "profile": {
                "first_name": "test_name",
                "last_name": "test_surname",
                "gender": "F",
                "birthday": "2000-12-30",
            },
        }

    def setUp(self):
        self.client = APIClient()
        return super().setUp()

    def test_successful_registration(self):
        response = self.client.post(self.user_create_url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # type: ignore
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(DatingProfile.objects.count(), 1)
        self.assertEqual(DatingUserNickname.objects.count(), 1)

    def test_registration_without_nickname(self):
        data = self.data.copy()
        del data["nickname"]
        response = self.client.post(self.user_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # type: ignore
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(DatingProfile.objects.count(), 1)
        self.assertEqual(DatingUserNickname.objects.count(), 0)

    def test_missing_required_field(self):
        data = self.data.copy()
        del data["profile"]["first_name"]
        response = self.client.post(self.user_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # type: ignore
        self.assertIn("first_name", response.data["profile"])  # type: ignore
        self.assertEqual(get_user_model().objects.count(), 0)
        self.assertEqual(DatingUserNickname.objects.count(), 0)
        self.assertEqual(DatingProfile.objects.count(), 0)

    def test_duplicate_email(self):
        self.client.post(self.user_create_url, self.data, format="json")
        data_dup = self.data.copy()
        del data_dup["nickname"]
        response = self.client.post(self.user_create_url, data_dup, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # type: ignore
        self.assertIn("email", response.data)  # type: ignore
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(DatingUserNickname.objects.count(), 1)
        self.assertEqual(DatingProfile.objects.count(), 1)

    def test_duplicate_nickname(self):
        self.client.post(self.user_create_url, self.data, format="json")
        data_dup = self.data.copy()
        data_dup["email"] = "user2@test.com"
        response = self.client.post(self.user_create_url, data_dup, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # type: ignore
        self.assertIn("nickname", response.data)  # type: ignore
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(DatingUserNickname.objects.count(), 1)
        self.assertEqual(DatingProfile.objects.count(), 1)

    def test_registration_invalid_email(self):
        data = deepcopy(self.data)
        data["email"] = "invalidemail"
        response = self.client.post(self.user_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # type: ignore
        self.assertIn("email", response.data)  # type: ignore
        self.assertEqual(get_user_model().objects.count(), 0)
        self.assertEqual(DatingUserNickname.objects.count(), 0)
        self.assertEqual(DatingProfile.objects.count(), 0)
