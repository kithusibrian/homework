# Shared Household Chores Tool

## Target users

Families with approximately 5-8 members.

## Confirmed decisions

- **Household membership:** Members join using a shared household code.
- **Assignment model:** Members choose available chores.
- **Completion:** Only the assigned member can mark a chore complete.
- **Reminders:** The tool sends automatic reminders for unfinished chores.
- **Schedule:** Chores repeat weekly.
- **Chore details:** Each chore has a name, description, frequency, and due date.
- **Changes:** Members can swap or decline assignments freely.

## Recommended MVP: four features to settle on

### 1. Household creation and joining

- One person creates a household.
- The tool generates a join code.
- Family members join with that code.
- Household members can see the shared chore board.

### 2. Weekly chore planning

- A household member creates weekly chores with the required details.
- Each chore appears as available until someone selects it.
- The board shows the current week's chores, due dates, and assignment status.

### 3. Self-assignment and chore completion

- Members select available chores for themselves.
- Members can freely swap or decline their assignments.
- Only the assigned member can mark a chore complete.
- Completed chores remain visible for the week.

### 4. Automatic overdue reminders

- The tool identifies chores that are still incomplete after their due date.
- It sends a reminder to the assigned member.
- Reminders should not be sent after the chore is completed or declined.

## Explicitly out of scope for the first version

- Complex fairness scoring or workload balancing
- Points, badges, or rewards
- Shopping lists and household finances
- Multiple households per account
- Custom recurrence beyond weekly chores
- Approval workflows for swaps or completion

## Main weekly workflow

1. A household member creates the week's chores.
2. Family members view available chores.
3. Members select chores for themselves.
4. Members complete their assigned chores.
5. The tool sends reminders for unfinished chores.
6. Members may swap or decline assignments as needed.
