from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Chore, Household, Membership


class HomeViewTests(TestCase):
	def test_home_page_returns_successful_response(self):
		response = self.client.get("/chores/")

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Household chores app is running.")


class HouseholdWorkflowTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(username="parent", password="password")
		self.client.login(username="parent", password="password")

	def test_user_can_create_household(self):
		response = self.client.post("/chores/households/create/", {"name": "The Home"})

		household = Household.objects.get(name="The Home")
		self.assertRedirects(response, f"/chores/households/{household.id}/")
		self.assertTrue(Membership.objects.filter(household=household, user=self.user).exists())
		self.assertEqual(len(household.join_code), 8)

	def test_user_can_join_household_with_code(self):
		household = Household.objects.create(name="The Home")

		response = self.client.post(
			"/chores/households/join/",
			{"join_code": household.join_code.lower()},
		)

		self.assertRedirects(response, f"/chores/households/{household.id}/")
		self.assertTrue(Membership.objects.filter(household=household, user=self.user).exists())


class ChoreWorkflowTests(TestCase):
	def setUp(self):
		user_model = get_user_model()
		self.user = user_model.objects.create_user(username="parent", password="password")
		self.other_user = user_model.objects.create_user(username="child", password="password")
		self.household = Household.objects.create(name="The Home")
		Membership.objects.create(household=self.household, user=self.user)
		Membership.objects.create(household=self.household, user=self.other_user)
		self.client.login(username="parent", password="password")

	def test_member_can_create_weekly_chore(self):
		response = self.client.post(
			f"/chores/households/{self.household.id}/chores/create/",
			{
				"name": "Wash dishes",
				"description": "Clean the kitchen after dinner.",
				"frequency": "weekly",
				"due_date": date.today() + timedelta(days=2),
			},
		)

		self.assertEqual(response.status_code, 302)
		chore = Chore.objects.get(name="Wash dishes")
		self.assertEqual(chore.household, self.household)
		self.assertEqual(chore.creator, self.user)
		self.assertEqual(chore.status, Chore.Status.AVAILABLE)

	def test_member_can_claim_and_complete_chore(self):
		chore = Chore.objects.create(
			household=self.household,
			creator=self.user,
			name="Take out bins",
			due_date=date.today(),
		)

		self.client.post(f"/chores/chores/{chore.id}/claim/")
		chore.refresh_from_db()
		self.assertEqual(chore.assignee, self.user)
		self.assertEqual(chore.status, Chore.Status.ASSIGNED)

		self.client.post(f"/chores/chores/{chore.id}/complete/")
		chore.refresh_from_db()
		self.assertEqual(chore.status, Chore.Status.COMPLETED)
		self.assertIsNotNone(chore.completed_at)

	def test_assigned_member_can_decline_and_another_member_can_claim(self):
		chore = Chore.objects.create(
			household=self.household,
			creator=self.user,
			assignee=self.user,
			name="Vacuum",
			due_date=date.today(),
			status=Chore.Status.ASSIGNED,
		)

		self.client.post(f"/chores/chores/{chore.id}/decline/")
		chore.refresh_from_db()
		self.assertEqual(chore.status, Chore.Status.DECLINED)
		self.assertIsNone(chore.assignee)

		self.client.login(username="child", password="password")
		self.client.post(f"/chores/chores/{chore.id}/claim/")
		chore.refresh_from_db()
		self.assertEqual(chore.status, Chore.Status.ASSIGNED)
		self.assertEqual(chore.assignee, self.other_user)

	def test_member_can_edit_chore(self):
		chore = Chore.objects.create(
			household=self.household,
			creator=self.user,
			name="Old name",
			due_date=date.today(),
		)

		response = self.client.post(
			f"/chores/chores/{chore.id}/edit/",
			{"name": "New name", "description": "Updated", "frequency": "weekly", "due_date": date.today()},
		)

		self.assertRedirects(response, f"/chores/households/{self.household.id}/")
		chore.refresh_from_db()
		self.assertEqual(chore.name, "New name")

	def test_only_assignee_can_complete_chore(self):
		chore = Chore.objects.create(
			household=self.household,
			creator=self.user,
			assignee=self.other_user,
			name="Clean bathroom",
			due_date=date.today(),
			status=Chore.Status.ASSIGNED,
		)

		response = self.client.post(f"/chores/chores/{chore.id}/complete/")

		self.assertEqual(response.status_code, 404)
		chore.refresh_from_db()
		self.assertEqual(chore.status, Chore.Status.ASSIGNED)
