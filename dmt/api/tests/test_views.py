from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from dmt.claim.models import Claim, PMTUser
from dmt.main.tests.factories import MilestoneFactory, ClientFactory


class AllProjectsViewTest(TestCase):
    def test_get(self):
        self.c = Client()
        r = self.c.get("/api/1.0/projects/all/")
        self.assertEqual(r.status_code, 200)


class AutoCompleteProjectViewTest(TestCase):
    def test_get(self):
        self.c = Client()
        r = self.c.get("/api/1.0/projects/autocomplete/?q=test")
        self.assertEqual(r.status_code, 200)


class AddTrackerViewTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.u = User.objects.create(username="testuser")
        self.u.set_password("test")
        self.u.save()
        self.c.login(username="testuser", password="test")
        pu = PMTUser.objects.create(username="testpmtuser",
                                    email="testemail@columbia.edu",
                                    status="active")
        Claim.objects.create(django_user=self.u, pmt_user=pu)
        m = MilestoneFactory()
        self.project = m.project

    def test_post_without_required_fields(self):
        r = self.c.post(
            "/api/1.0/trackers/add/",
            dict())
        self.assertEqual(r.status_code, 200)

    def test_post(self):
        r = self.c.post(
            "/api/1.0/trackers/add/",
            dict(
                pid=self.project.pid,
                task="test",
                time="1 hour",
            ))
        self.assertEqual(r.status_code, 200)

    def test_post_with_nonexistant_client(self):
        r = self.c.post(
            "/api/1.0/trackers/add/",
            dict(
                pid=self.project.pid,
                task="test",
                time="1 hour",
                client="foo",
            ))
        self.assertEqual(r.status_code, 200)

    def test_post_with_client(self):
        self.client = ClientFactory()
        r = self.c.post(
            "/api/1.0/trackers/add/",
            dict(
                pid=self.project.pid,
                task="test",
                time="1 hour",
                client="testclient",
            ))
        self.assertEqual(r.status_code, 200)
