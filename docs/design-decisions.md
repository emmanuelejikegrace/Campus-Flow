# WHERE IS THE TICKET COLLECTOIN STORED AND HOW  IS IT PASSED BETWEEN FUNCTIONS: 

in our CampusFlow CLI project, the ticket collection lives in two places depending on whether the program is running or closed, and it moves through our code using Python objects and memory references. 

# where the Ticket Collection is Stored:
- When the CampusFlow is Closed(On disk); it is stored in tickets.json file
- When the CampusFlow is Running(in Memory); it is stored in ticketManager.py file 

# How the Collection is Passed Betweeen Functions

Instead of constantly moving the entire list of tickets back and forth—which is slow and messy—Python uses specific techniques to handle data flow between your function:

- PASSING BY REFERENCE (in-memory Access) 
e.g; A function called find_ticket(ticket_id) searches your central list and returns the matching ticket object.
 
- THE "DATA TRANSFER OBJECT"(DTO) PATTERN
e.g; Your CLI parsing function gathers user inputs from the terminal.It packages these inputs into a temporary package (either a Python dictionary or a small Ticket instance).
it passes this single package to your add_ticket() function, which assigns it a unique ID, stamps the time, and appends it to the main collection.

# HOW DOES A FUNCTION SIGNAL INPUT(EXCEPTION OR STRUCTURED ERROR), AND HOW DOES THE CLI DISPLAY IT?


How a Function Signals Invalid Input

Functions signal errors using Python Exceptions.
Instead of returning a broken value, the business logic function explicitly raises a built-in or custom exception [health]. This immediately stops execution and passes the error message up to the caller.


How the CLI Displays It

The CLI layer handles this using a Try-Except Block.
It catches the exception [health], prevents the program from crashing rudely, and prints a clean, user-friendly error message to the terminal (often styled with color or a clear indicator).

# WHAT IS THE EXPECTED RETURN VALUE WHEN A TICKET IS CREATED, ASSIGNED, OR UPDATED

* When Created: Returns the new ticket's details, including its unique ID and initial status.

* When Assigned: Returns the updated ticket with the assigned user's ID or name.

* When Updated: Returns the ticket with the modified fields and current status.

* On failure: Raises an exception or returns a structured error explaining the problem.

