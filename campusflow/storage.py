import json
from pathlib import Path

from campusflow.tickets import Ticket


DEFAULT_FILE = Path("data/tickets.json")


def save_tickets(tickets, filepath=DEFAULT_FILE):
    """
    Save a collection of Ticket objects to a JSON file.
    """

    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    ticket_data = [
        ticket.to_dict()
        for ticket in tickets
    ]

    with filepath.open("w", encoding="utf-8") as file:
        json.dump(ticket_data, file, indent=4)

    return True


def load_tickets(filepath=DEFAULT_FILE):
    """
    Load tickets from a JSON file.

    Return an empty list if the file does not exist.
    Raise a clear error if the JSON is malformed.
    """

    filepath = Path(filepath)

    if not filepath.exists():
        return []

    try:
        with filepath.open("r", encoding="utf-8") as file:
            ticket_data = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Cannot load tickets from {filepath}: "
            f"the JSON file is malformed."
        ) from error

    if not isinstance(ticket_data, list):
        raise ValueError(
            f"Cannot load tickets from {filepath}: "
            f"the JSON root must be a list."
        )

    loaded_tickets = []

    for item in ticket_data:
        if not isinstance(item, dict):
            raise ValueError(
                "Cannot load tickets: each ticket must be a JSON object."
            )

        required_fields = {
            "id",
            "title",
            "category",
            "urgency",
            "affected_users",
            "priority",
            "status",
            "assigned_to",
        }

        if not required_fields.issubset(item):
            raise ValueError(
                "Cannot load tickets: a ticket is missing required fields."
            )

        ticket = Ticket(
            title=item["title"],
            category=item["category"],
            urgency=item["urgency"],
            affected_users=item["affected_users"],
        )

        # Restore the saved values.
        ticket.id = item["id"]
        ticket.priority = item["priority"]
        ticket.status = item["status"]
        ticket.assigned_to = item["assigned_to"]

        loaded_tickets.append(ticket)

    ids = [ticket.id for ticket in loaded_tickets]

    if len(ids) != len(set(ids)):
        raise ValueError(
            "Cannot load tickets: duplicate ticket IDs were found."
        )

    return loaded_tickets


def load_into_manager(manager, filepath=DEFAULT_FILE):
    """
    Load saved tickets into an existing TicketManager.

    Also update the next ID counter to avoid duplicate IDs.
    """

    loaded_tickets = load_tickets(filepath)

    manager.tickets = loaded_tickets

    numeric_ids = []

    for ticket in loaded_tickets:
        ticket_id = ticket.id

        if (
            isinstance(ticket_id, str)
            and ticket_id.startswith("T")
            and ticket_id[1:].isdigit()
        ):
            numeric_ids.append(int(ticket_id[1:]))

    if numeric_ids:
        manager.next_id_counter = max(numeric_ids) + 1
    else:
        manager.next_id_counter = 1

    return len(loaded_tickets)