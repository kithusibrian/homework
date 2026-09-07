from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ChoreForm, HouseholdForm, JoinHouseholdForm
from .models import Chore, Household, Membership


def home(request):
	return HttpResponse("Household chores app is running.")


def household_membership(request, household_id):
	return get_object_or_404(Membership, household_id=household_id, user=request.user)


@login_required
def create_household(request):
	form = HouseholdForm(request.POST or None)
	if request.method == "POST" and form.is_valid():
		household = form.save()
		Membership.objects.create(household=household, user=request.user)
		return redirect("chores:board", household_id=household.id)
	return render(request, "chores/household_form.html", {"form": form, "title": "Create household"})


@login_required
def join_household(request):
	form = JoinHouseholdForm(request.POST or None)
	if request.method == "POST" and form.is_valid():
		household = Household.objects.filter(join_code=form.cleaned_data["join_code"].upper()).first()
		if household is None:
			form.add_error("join_code", "No household uses that code.")
		else:
			try:
				Membership.objects.create(household=household, user=request.user)
			except IntegrityError:
				form.add_error(None, "You already belong to this household.")
			else:
				return redirect("chores:board", household_id=household.id)
	return render(request, "chores/household_form.html", {"form": form, "title": "Join household"})


@login_required
def board(request, household_id):
	membership = household_membership(request, household_id)
	chores = membership.household.chores.select_related("assignee").order_by("status", "due_date", "name")
	return render(request, "chores/board.html", {"household": membership.household, "chores": chores})


@login_required
def create_chore(request, household_id):
	membership = household_membership(request, household_id)
	form = ChoreForm(request.POST or None)
	if request.method == "POST" and form.is_valid():
		chore = form.save(commit=False)
		chore.household = membership.household
		chore.creator = request.user
		chore.save()
		return redirect("chores:board", household_id=household_id)
	return render(request, "chores/chore_form.html", {"form": form, "household": membership.household})


@login_required
def edit_chore(request, chore_id):
	chore = get_object_or_404(Chore, pk=chore_id)
	membership = household_membership(request, chore.household_id)
	form = ChoreForm(request.POST or None, instance=chore)
	if request.method == "POST" and form.is_valid():
		form.save()
		return redirect("chores:board", household_id=chore.household_id)
	return render(request, "chores/chore_form.html", {"form": form, "household": membership.household, "chore": chore})


@login_required
def claim_chore(request, chore_id):
	chore = get_object_or_404(Chore, pk=chore_id)
	household_membership(request, chore.household_id)
	if request.method == "POST" and chore.status in [Chore.Status.AVAILABLE, Chore.Status.DECLINED]:
		chore.assignee = request.user
		chore.status = Chore.Status.ASSIGNED
		chore.declined_at = None
		chore.save(update_fields=["assignee", "status", "declined_at"])
	return redirect("chores:board", household_id=chore.household_id)


@login_required
def complete_chore(request, chore_id):
	chore = get_object_or_404(Chore, pk=chore_id, assignee=request.user)
	household_membership(request, chore.household_id)
	if request.method == "POST" and chore.status == Chore.Status.ASSIGNED:
		chore.mark_completed()
	return redirect("chores:board", household_id=chore.household_id)


@login_required
def decline_chore(request, chore_id):
	chore = get_object_or_404(Chore, pk=chore_id, assignee=request.user)
	household_membership(request, chore.household_id)
	if request.method == "POST" and chore.status == Chore.Status.ASSIGNED:
		chore.assignee = None
		chore.status = Chore.Status.DECLINED
		chore.declined_at = timezone.now()
		chore.save(update_fields=["assignee", "status", "declined_at"])
	return redirect("chores:board", household_id=chore.household_id)
