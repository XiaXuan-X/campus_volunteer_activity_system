from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from accounts.models import User
from activities.models import Activity
from organiser.models import Application


class ModelTests(TestCase):
    """
    These tests verify the core business logic of the Application model,
    including creation, status updates and uniqueness constraints.
    """

    def setUp(self):
        # Create an organiser user
        self.organiser = User.objects.create_user(
            username="org1",
            password="test1234",
            role="organiser"
        )

        # Create a volunteer user
        self.volunteer = User.objects.create_user(
            username="vol1",
            password="test1234",
            role="volunteer"
        )

        # Create a valid activity
        self.activity = Activity.objects.create(
            title="Food Bank",
            description="Help sorting food",
            location="Glasgow",
            start_datetime=timezone.now() - timedelta(hours=1),
            end_datetime = timezone.now() + timedelta(hours=2),
            max_volunteers=5,
            organiser=self.organiser
        )

    def test_organiser_can_create_activity(self):
        """
        Test that an organiser can create an activity successfully.
        """
        activity = Activity.objects.create(
            title="Test Activity",
            description="Test description",
            location="Glasgow",
            start_datetime=timezone.now() - timedelta(hours=1),
            end_datetime=timezone.now() + timedelta(hours=2),
            max_volunteers=10,
            organiser=self.organiser
        )

        self.assertEqual(activity.organiser, self.organiser)
        self.assertEqual(activity.title, "Test Activity")

    def test_application_creation(self):
        """
        Test that a new application can be created successfully
        with the default status.
        """
        application = Application.objects.create(
            volunteer=self.volunteer,
            activity=self.activity,
            status="pending"
        )

        self.assertEqual(application.status, "pending")
        self.assertEqual(application.volunteer, self.volunteer)

    def test_duplicate_application_not_allowed(self):
        """
        Test that a volunteer cannot apply for the same activity twice,
        based on the unique_together constraint.
        """
        Application.objects.create(
            volunteer=self.volunteer,
            activity=self.activity
        )

        with self.assertRaises(Exception):
            Application.objects.create(
                volunteer=self.volunteer,
                activity=self.activity
            )

    def test_cancel_application(self):
        """
        Test that a pending application can be updated to cancelled.
        """
        application = Application.objects.create(
            volunteer=self.volunteer,
            activity=self.activity,
            status="pending"
        )

        application.status = "cancelled"
        application.save()

        application.refresh_from_db()
        self.assertEqual(application.status, "cancelled")

    def test_approve_application(self):
        """
        Test that an application status can be updated to approved.
        """
        application = Application.objects.create(
            volunteer=self.volunteer,
            activity=self.activity,
            status="pending"
        )

        application.status = "approved"
        application.save()

        application.refresh_from_db()
        self.assertEqual(application.status, "approved")



class ViewTests(TestCase):
    """
    These tests simulate user interactions with the system,
    specifically testing the apply view to ensure that
    end-to-end behaviour works correctly.
    """

    def setUp(self):
        self.client = Client()

        # Create organiser user
        self.organiser = User.objects.create_user(
            username="org1",
            password="test1234",
            role="organiser"
        )

        # Create volunteer user
        self.volunteer = User.objects.create_user(
            username="vol1",
            password="test1234",
            role="volunteer"
        )

        # Create an activity that is currently open for application
        self.activity = Activity.objects.create(
            title="Beach Cleanup",
            description="Community work",
            location="Glasgow",
            start_datetime=timezone.now() - timedelta(hours=1),
            end_datetime=timezone.now() + timedelta(hours=2),
            max_volunteers=2,
            organiser=self.organiser
        )

    def test_volunteer_can_apply(self):
        """
        Test that a logged-in volunteer can apply for an activity
        and that the application is correctly stored in the database.
        """
        login_success = self.client.login(username="vol1", password="test1234")
        self.assertTrue(login_success)

        response = self.client.post(
            reverse("activities:apply", args=[self.activity.id])
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Application.objects.filter(
                volunteer=self.volunteer,
                activity=self.activity
            ).exists()
        )