PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}


def get_work_queue(tickets):
    """
    Return open tickets sorted by priority and then numeric ticket ID.

    Priority order:
    critical -> high -> medium -> low
    """

    open_tickets = [
        ticket
        for ticket in tickets
        if ticket.status == "open"
    ]

    return sorted(
        open_tickets,
        key=lambda ticket: (
            PRIORITY_ORDER[ticket.priority],
            int(ticket.id[1:])
        )
    )

    def generate_report(tickets):
    """
    Return a report containing total tickets,
    ticket counts by status, and ticket counts by priority.
    """

    status_counts = {
        "open": 0,
        "in_progress": 0,
        "resolved": 0,
    }

    priority_counts = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for ticket in tickets:
        status_counts[ticket.status] += 1
        priority_counts[ticket.priority] += 1

    return {
        "total_tickets": len(tickets),
        "by_status": status_counts,
        "by_priority": priority_counts,
    }