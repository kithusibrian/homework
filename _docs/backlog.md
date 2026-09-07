# Shared Household Chores Tool Backlog

A small, ordered MVP backlog based on the agreed scope. Complete tasks from top to bottom unless noted otherwise.

## B01. Configure the chores app

**Goal:** Prepare the Django app for feature development.

**Tasks:**

- Confirm `chores` is included in `INSTALLED_APPS`.
- Add app URL routing and a basic health-check or home view.
- Add a minimal test setup for the app.

**Acceptance criteria:**

- `python manage.py check` passes.
- The app has a working URL that returns a successful response.

## B02. Create the household and membership model

**Goal:** Support one household with 5-8 family members joining by code.

**Tasks:**

- Add a `Household` model with a name and unique join code.
- Connect Django users to households through a membership model or profile relationship.
- Add forms or views to create a household and join one with a code.
- Add migrations and model tests.

**Depends on:** B01

**Acceptance criteria:**

- A household can be created with a unique join code.
- A valid code lets a user join the household.
- An invalid or duplicate join attempt is rejected clearly.

## B03. Build weekly chore planning

**Goal:** Let a household member create and view the week's chores.

**Tasks:**

- Add a `Chore` model with name, description, frequency, due date, household, creator, and status.
- Restrict the first version to weekly chores.
- Create a household chore-board view showing available and assigned chores.
- Add create and edit forms with validation.
- Add migrations and model/form tests.

**Depends on:** B02

**Acceptance criteria:**

- A household member can create a weekly chore with the required details.
- Only members of the household can view or change its chores.
- The board shows the current week's chores and due dates.

## B04. Add self-assignment and completion

**Goal:** Let family members claim, change, and complete chores.

**Tasks:**

- Allow a member to claim an available chore for themselves.
- Allow an assigned member to decline or swap their chore freely.
- Allow only the assigned member to mark a chore complete.
- Record assignment and completion timestamps.
- Add permission and workflow tests.

**Depends on:** B03

**Acceptance criteria:**

- A member can claim an available chore.
- An assigned member can decline or swap it without approval.
- Another member cannot mark someone else's chore complete.
- Completed chores remain visible for the week.

## B05. Implement overdue reminders

**Goal:** Notify members about unfinished chores after the due date.

**Tasks:**

- Add a reminder service or management command that finds overdue, incomplete chores.
- Send a reminder to the assigned member.
- Do not remind for completed or declined chores.
- Prevent duplicate reminders for the same overdue event.
- Add tests using Django's email test backend.

**Depends on:** B04

**Acceptance criteria:**

- An overdue assigned chore produces one reminder for its assignee.
- Completed and declined chores produce no reminder.
- Running the reminder process again does not send a duplicate reminder unnecessarily.

## B06. Harden the MVP and document local use

**Goal:** Make the first version runnable and reviewable.

**Tasks:**

- Add end-to-end tests for create, join, claim, complete, decline, and reminder flows.
- Add useful empty, error, and permission states to the views.
- Run migrations, the full test suite, and Django checks.
- Update the README with setup and local run instructions.

**Depends on:** B01-B05

**Acceptance criteria:**

- The full test suite passes.
- `python manage.py check` passes.
- A new developer can run the project and follow the documented weekly workflow.

## Deferred backlog

These items remain outside the first version:

- Fairness scoring or workload balancing
- Points, badges, or rewards
- Shopping lists and household finances
- Multiple households per account
- Custom recurrence beyond weekly chores
- Approval workflows for swaps or completion
