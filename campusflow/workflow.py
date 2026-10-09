from campusflow.tickets import Ticket

class TicketManager:
    def __init__(self):
        # Master list holding all active Ticket objects in memory
        self.tickets = []
        # Internal sequential counter to guarantee unique IDs (F1 / F7 continuity)
        self.next_id_counter = 1

    def _generate_next_id(self) -> str:
        """Generates a padded string unique ID. Example: 1 -> 'T001'"""
        ticket_id = f"T{self.next_id_counter:03d}"
        self.next_id_counter += 1
        return ticket_id

    def create_ticket(self, title: str, category: str, urgency: str, affected_users: int) -> Ticket:
        """
        F1: Creates, validates, stamps an ID, and stores a new ticket.
        Returns the fully formed Ticket object.
        """
        # Create a new ticket instance. (Validations are handled inside Ticket.__init__)
        new_ticket = Ticket(
            title=title, 
            category=category, 
            urgency=urgency, 
            affected_users=affected_users
        )
        
        # Stamp with a system-controlled unique sequential ID
        new_ticket.id = self._generate_next_id()
        
        # Append to our in-memory data collection
        self.tickets.append(new_ticket)
        return new_ticket

    def find_ticket_by_id(self, ticket_id: str) -> Ticket:
        """
        Helper method to locate an exact ticket instance in memory.
        Raises ValueError if the ID does not exist (F3 requirement).
        """
        # Normalize the requested ID format just in case (e.g. 't001' -> 'T001')
        target_id = ticket_id.strip().upper()
        
        for ticket in self.tickets:
            if ticket.id == target_id:
                return ticket
                
        raise ValueError(f"Ticket ID '{ticket_id}' not found in the system.")

    def assign_ticket(self, ticket_id: str, staff_name: str) -> Ticket:
        """
        F3/F4: Assigns a ticket to a staff member.
        Rejects empty assignee names and locked resolved tickets.
        """
        # Clean the staff name input
        if not staff_name or not staff_name.strip():
            raise ValueError("Assignee name cannot be blank.")
        
        # Find the ticket (will throw ValueError if ID is invalid)
        ticket = self.find_ticket_by_id(ticket_id)
        
        # F4 Guardrail: Block changes to resolved tickets unless reopened
        if ticket.status == "resolved":
            raise ValueError("Cannot assign a resolved ticket. You must reopen it first.")
            
        ticket.assigned_to = staff_name.strip()
        return ticket

    def update_status(self, ticket_id: str, new_status: str) -> Ticket:
        """
        F4: Progresses a ticket's status through 'open', 'in_progress', or 'resolved'.
        Enforces state transition constraints.
        """
        ticket = self.find_ticket_by_id(ticket_id)
        
        # Normalize status input (e.g. 'IN_PROGRESS' -> 'in_progress')
        normalized_status = new_status.strip().lower()
        
        if normalized_status not in {"open", "in_progress", "resolved"}:
            raise ValueError("Status must be either 'open', 'in_progress', or 'resolved'.")
            
        # F4 Guardrail: Block modification on resolved tickets
        if ticket.status == "resolved":
            raise ValueError("This ticket is resolved and locked. You must explicitly reopen it.")
            
        # F4 Guardrail: Do not move an unassigned ticket into 'in_progress'
        if normalized_status == "in_progress" and ticket.assigned_to is None:
            raise ValueError("Cannot move a ticket to 'In Progress' without an assigned staff member.")
            
        ticket.status = normalized_status
        return ticket

    def reopen_ticket(self, ticket_id: str) -> Ticket:
        """
        F4: Explicitly breaks the lock on a resolved ticket,
        reverting its state back to 'open' for editing.
        """
        ticket = self.find_ticket_by_id(ticket_id)
        
        if ticket.status != "resolved":
            raise ValueError("Only tickets with a status of 'resolved' can be reopened.")
            
        ticket.status = "open"
        return ticket
