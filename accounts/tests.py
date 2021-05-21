from django.test import TestCase
from django.contrib.auth import get_user_model


class UserAccountTests(TestCase):

    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            "testsuperuser@Gmail.com", "1234"
        )
        self.assertEqual(super_user.email, "testsuperuser@gmail.com")
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email="testsuperuser@gmail.com", password="1234", is_superuser=False, first_name="Tanvir"
            )
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email="testsuperuser@gmail.com", password="1234", is_staff=False, first_name="Tanvir"
            )
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email="", password="1234", is_superuser=True, first_name="Tanvir"
            )

    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            email="testuser@gmail.com", password="1234"
        )
        self.assertEqual(user.email, "testuser@gmail.com")
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        # self.assertFalse(user.is_active)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email="", password="1234", first_name="Tanvir")
