from django.db import IntegrityError
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from user.models import User
from user.serializers import AuthTokenSerializer, UserSerializer


class UserCreationTests(APITestCase):
    def test_create_user(self):
        url = reverse('user:create')
        data = {
            'email': 'test@example.com',
            'password': 'password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')

    def test_create_user_with_existing_email(self):
        User.objects.create_user(
            email='test@example.com',
            password='password'
        )
        url = reverse('user:create')
        data = {
            'email': 'test@example.com',
            'password': 'password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SuperuserCreationTests(APITestCase):
    def test_create_superuser(self):
        User.objects.create_superuser(
            email='admin@example.com',
            password='password',
            is_staff=True,
            is_superuser=True
        )

        self.assertTrue(User.objects.get(email='admin@example.com').is_superuser)

    def test_create_superuser_with_existing_email(self):
        User.objects.create_superuser(
            email='admin@example.com',
            password='password',
            is_staff=True,
            is_superuser=True
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_superuser(
                email='admin@example.com',
                password='password',
                is_staff=True,
                is_superuser=True
            )


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class TestTokenObtainPairView(APITestCase):

    def setUp(self):
        self.user = create_user(
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_token_obtain_pair_view(self):
        url = reverse('user:token_obtain_pair')
        refresh_url = reverse('user:token_refresh')
        verify_url = reverse('user:token_verify')
        data = {
            "email": "test@test.com",
            "password": "testpass"
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == 200
        refresh_token = response.data.get('refresh')
        new_response = self.client.post(refresh_url, {"refresh": refresh_token}, format='json')
        assert new_response.status_code == 200
        verify_token = self.client.post(verify_url, {"token": refresh_token}, format='json')
        assert verify_token.status_code == 200

        assert refresh_token is not None
        access_token = response.data.get('access')
        assert access_token is not None


class UserSerializerTest(APITestCase):
    def setUp(self):
        self.validated_data = {
            'email': 'test@example.com',
            'password': 'password',
            'is_staff': False
        }

    def test_create_user(self):
        serializer = UserSerializer(data=self.validated_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.email, self.validated_data['email'])
        self.assertTrue(user.check_password(self.validated_data['password']))

    def test_update_user(self):
        user = get_user_model().objects.create_user(**self.validated_data)
        serializer = UserSerializer(user, data={'email': 'new@example.com'}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertEqual(updated_user.email, 'new@example.com')


class AuthTokenSerializerTest(APITestCase):
    def setUp(self):
        self.email = 'test@example.com'
        self.password = 'password'
        self.user = get_user_model().objects.create_user(
            email=self.email,
            password=self.password
        )

    def test_authenticate_user(self):
        serializer = AuthTokenSerializer(data={
            'email': self.email,
            'password': self.password
        })
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data

        self.assertEqual(validated_data['user'], self.user)

    def test_invalid_credentials(self):
        serializer = AuthTokenSerializer(data={
            'email': self.email,
            'password': 'wrongpassword'
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn('Unable to log in', str(serializer.errors))
