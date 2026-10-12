from campusflow.reports import get_work_queue


def show_work_queue(manager):
    queue = get_work_queue(manager.tickets)

    if not queue:
        print("\nNo open tickets in the work queue.")
        return

    print("\n========== WORK QUEUE ==========")

    for ticket in queue:
        print(f"\nID: {ticket.id}")
        print(f"Title: {ticket.title}")
        print(f"Priority: {ticket.priority}")
        print(f"Status: {ticket.status}")
        print(f"Assigned To: {ticket.assigned_to}")


 # Add another help

from campusflow.reports import generate_report
def show_reports(manager):
    report = generate_report(manager.tickets)

    print("\n========== CAMPUSFLOW REPORT ==========")

    print(f"\nTotal Tickets: {report['total_tickets']}")

    print("\nTickets by Status:")

    for status, count in report["by_status"].items():
        print(f"{status.replace('_', ' ').title()}: {count}")

    print("\nTickets by Priority:")

    for priority, count in report["by_priority"].items():
        print(f"{priority.title()}: {count}")