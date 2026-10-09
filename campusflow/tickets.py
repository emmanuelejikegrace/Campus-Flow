# campusflow/tickets.py

ALLOWED_CATEGORIES = {"Network", "Hardware", "Software", "Other"}
ALLOWED_URGENCIES = {"low", "medium", "high"}

def normalize_category(category_str: str) -> str:
    if not category_str:
        raise ValueError("Category cannot be blank.")
    
    normalized = category_str.strip().capitalize()
    
    if normalized not in ALLOWED_CATEGORIES:
        raise ValueError(f"Invalid category '{category_str}'. Must be one of: {', '.join(ALLOWED_CATEGORIES)}")
        
    return normalized

def normalize_urgency(urgency_str: str) -> str:
    if not urgency_str:
        raise ValueError("Urgency cannot be blank.")
        
    normalized = urgency_str.strip().lower()
    
    if normalized not in ALLOWED_URGENCIES:
        raise ValueError(f"Invalid urgency '{urgency_str}'. Must be one of: {', '.join(ALLOWED_URGENCIES)}")
        
    return normalized

def validate_title(title_str: str) -> str:
    if not title_str or not title_str.strip():
        raise ValueError("Ticket title cannot be blank.")
    return title_str.strip()

def validate_affected_users(users_input) -> int:
    
    if isinstance(users_input, bool):
        raise ValueError("Affected users must be a valid positive whole number.")

    try:
        if isinstance(users_input, float):
            if not users_input.is_integer():
                raise ValueError("Affected users cannot be a decimal number.")
            users_val = int(users_input)
        else:
            users_val = int(users_input)
    except (ValueError, TypeError):
        raise ValueError("Affected users must be a numeric whole number.")

    if users_val <= 0:
        raise ValueError("Affected users must be a positive integer greater than zero.")
        
    return users_val

class Ticket:
    def __init__(self, title: str, category: str, urgency: str, affected_users: int):
        # 1. Validate and Normalize inputs immediately using our Step 1 filters
        self.title = validate_title(title)
        self.category = normalize_category(category)
        self.urgency = normalize_urgency(urgency)
        self.affected_users = validate_affected_users(affected_users)
        
        # 2. System-managed fields initialized automatically
        self.id = None         
        self.assigned_to = None 
        self.status = "open"    
        
        # 3. Automatically calculate priority matrix (F1 requirement)
        self.priority = self._calculate_priority()

    def _calculate_priority(self) -> str:
        """
        Matrix Logic: Combines urgency and scale of impact (affected users)
        to determine the final engineering priority.
        """
        # Critical Tier Rule
        if self.urgency == "high" and self.affected_users >= 10:
            return "critical"
        
        # High Tier Rule
        elif self.urgency == "high" or (self.urgency == "medium" and self.affected_users >= 5):
            return "high"
        
        # Medium Tier Rule
        elif self.urgency == "medium" or (self.urgency == "low" and self.affected_users >= 5):
            return "medium"
        
        # Default Low Tier
        else:
            return "low"

    def to_dict(self) -> dict:
        """Converts the internal object data into a clean dictionary format for JSON saving."""
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "urgency": self.urgency,
            "affected_users": self.affected_users,
            "priority": self.priority,
            "status": self.status,
            "assigned_to": self.assigned_to
        }
