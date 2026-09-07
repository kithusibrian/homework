from django.urls import path

from . import views


app_name = "chores"

urlpatterns = [
    path("", views.home, name="home"),
    path("households/create/", views.create_household, name="create_household"),
    path("households/join/", views.join_household, name="join_household"),
    path("households/<int:household_id>/", views.board, name="board"),
    path("households/<int:household_id>/chores/create/", views.create_chore, name="create_chore"),
    path("chores/<int:chore_id>/edit/", views.edit_chore, name="edit_chore"),
    path("chores/<int:chore_id>/claim/", views.claim_chore, name="claim_chore"),
    path("chores/<int:chore_id>/complete/", views.complete_chore, name="complete_chore"),
    path("chores/<int:chore_id>/decline/", views.decline_chore, name="decline_chore"),
]