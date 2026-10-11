import unittest

from campusflow.workflow import TicketManager
from campusflow.reports import get_work_queue, generate_report


class TestWorkQueue(unittest.TestCase):

    def setUp(self):
        self.manager = TicketManager()

        # Create four tickets.
        self.manager.create_ticket(
            "Low priority issue",
            "Software",
            "low",
            1,
        )

        self.manager.create_ticket(
            "Critical network issue",
            "Network",
            "high",
            15,
        )

        self.manager.create_ticket(
            "High priority issue",
            "Hardware",
            "high",
            2,
        )

        self.manager.create_ticket(
            "Medium priority issue",
            "Software",
            "low",
            4,
        )

    def test_queue_orders_by_priority(self):
        queue = get_work_queue(self.manager.tickets)

        priorities = [
            ticket.priority
            for ticket in queue
        ]

        self.assertEqual(
            priorities,
            ["critical", "high", "medium", "low"],
        )

    def test_queue_excludes_non_open_tickets(self):
        self.manager.tickets[0].status = "resolved"
        self.manager.tickets[2].status = "in_progress"

        queue = get_work_queue(self.manager.tickets)

        statuses = [
            ticket.status
            for ticket in queue
        ]

        self.assertTrue(
            all(status == "open" for status in statuses)
        )

        self.assertEqual(len(queue), 2)

    def test_queue_uses_numeric_id_for_ties(self):
        # The first two tickets both have high priority.
        # Their numeric IDs should determine their order.
        self.manager.tickets[1].priority = "high"

        queue = get_work_queue(self.manager.tickets)

        high_tickets = [
            ticket
            for ticket in queue
            if ticket.priority == "high"
        ]

        numeric_ids = [
            int(ticket.id[1:])
            for ticket in high_tickets
        ]

        self.assertEqual(
            numeric_ids,
            sorted(numeric_ids),
        )

    def test_empty_queue(self):
        queue = get_work_queue([])

        self.assertEqual(queue, [])


class TestReports(unittest.TestCase):

    def test_empty_report(self):
        report = generate_report([])

        self.assertEqual(report["total_tickets"], 0)

        self.assertEqual(
            report["by_status"],
            {
                "open": 0,
                "in_progress": 0,
                "resolved": 0,
            },
        )

        self.assertEqual(
            report["by_priority"],
            {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
            },
        )

    def test_report_counts_tickets(self):
        manager = TicketManager()

        manager.create_ticket(
            "Network outage",
            "Network",
            "high",
            15,
        )

        manager.create_ticket(
            "Keyboard problem",
            "Hardware",
            "low",
            1,
        )

        manager.tickets[1].status = "resolved"

        report = generate_report(manager.tickets)

        self.assertEqual(report["total_tickets"], 2)

        self.assertEqual(
            report["by_status"]["open"],
            1,
        )

        self.assertEqual(
            report["by_status"]["resolved"],
            1,
        )

        self.assertEqual(
            report["by_priority"]["critical"],
            1,
        )

        self.assertEqual(
            report["by_priority"]["low"],
            1,
        )


if __name__ == "__main__":
    unittest.main()