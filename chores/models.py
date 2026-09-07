import secrets
import string

from django.conf import settings
from django.db import models
from django.utils import timezone


def generate_join_code():
	alphabet = string.ascii_uppercase + string.digits
	return "".join(secrets.choice(alphabet) for _ in range(8))


class Household(models.Model):
	name = models.CharField(max_length=100)
	join_code = models.CharField(max_length=8, unique=True, default=generate_join_code)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class Membership(models.Model):
	household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name="memberships")
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="household_memberships")
	joined_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=["household", "user"], name="unique_household_member"),
		]


class Chore(models.Model):
	class Status(models.TextChoices):
		AVAILABLE = "available", "Available"
		ASSIGNED = "assigned", "Assigned"
		COMPLETED = "completed", "Completed"
		DECLINED = "declined", "Declined"

	household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name="chores")
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_chores")
	assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_chores")
	name = models.CharField(max_length=150)
	description = models.TextField(blank=True)
	frequency = models.CharField(max_length=20, default="weekly")
	due_date = models.DateField()
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
	completed_at = models.DateTimeField(null=True, blank=True)
	declined_at = models.DateTimeField(null=True, blank=True)
	reminder_sent_at = models.DateTimeField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def mark_completed(self):
		self.status = self.Status.COMPLETED
		self.completed_at = timezone.now()
		self.save(update_fields=["status", "completed_at"])
