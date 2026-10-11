import json
import tempfile
import unittest

from pathlib import Path

from campusflow.workflow import TicketManager
from campusflow.storage import save_tickets, load_tickets


class TestTicketStorage(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.filepath = (
            Path(self.temp_dir.name) / "tickets.json"
        )

        self.manager = TicketManager()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_and_load_tickets(self):
        self.manager.create_ticket(
            "Campus Wi-Fi is down",
            "Network",
            "high",
            15,
        )

        save_tickets(
            self.manager.tickets,
            self.filepath,
        )

        loaded_tickets = load_tickets(self.filepath)

        self.assertEqual(len(loaded_tickets), 1)

        original = self.manager.tickets[0]
        loaded = loaded_tickets[0]

        self.assertEqual(loaded.id, original.id)
        self.assertEqual(loaded.title, original.title)
        self.assertEqual(loaded.priority, original.priority)
        self.assertEqual(loaded.status, original.status)
        self.assertEqual(
            loaded.assigned_to,
            original.assigned_to,
        )

    def test_missing_file_returns_empty_list(self):
        missing_file = (
            Path(self.temp_dir.name) / "missing.json"
        )

        loaded_tickets = load_tickets(missing_file)

        self.assertEqual(loaded_tickets, [])

    def test_malformed_json_raises_clear_error(self):
        self.filepath.write_text(
            "{this is not valid JSON",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            ValueError,
            "JSON file is malformed",
        ):
            load_tickets(self.filepath)

    def test_duplicate_ids_are_rejected(self):
        self.manager.create_ticket(
            "First ticket",
            "Network",
            "high",
            15,
        )

        self.manager.create_ticket(
            "Second ticket",
            "Hardware",
            "low",
            1,
        )

        tickets_data = [
            ticket.to_dict()
            for ticket in self.manager.tickets
        ]

        tickets_data[1]["id"] = tickets_data[0]["id"]

        self.filepath.write_text(
            json.dumps(tickets_data),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            ValueError,
            "duplicate ticket IDs",
        ):
            load_tickets(self.filepath)

    def test_new_id_is_unique_after_reload(self):
        self.manager.create_ticket(
            "First ticket",
            "Network",
            "high",
            15,
        )

        save_tickets(
            self.manager.tickets,
            self.filepath,
        )

        reloaded_manager = TicketManager()

        reloaded_manager.load(self.filepath)

        new_ticket = reloaded_manager.create_ticket(
            "Second ticket",
            "Hardware",
            "low",
            1,
        )

        self.assertEqual(new_ticket.id, "T002")

        existing_ids = [
            ticket.id
            for ticket in reloaded_manager.tickets
        ]

        self.assertEqual(
            len(existing_ids),
            len(set(existing_ids)),
        )


if __name__ == "__main__":
    unittest.main()