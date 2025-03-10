# T7

Two-Tier Architecture: SQLite and Python Server-Client
Summary of the Activity
This project implements a Two-Tier Architecture using Python and SQLite. It consists of:

A Python-based server that manages a SQLite database.
A Python client interface that interacts with the server through TCP communication.
The application allows users to Create, Read, Update, and Delete (CRUD) notes in a database. The server processes requests while the client sends commands to perform operations on the database.

Instructions for Running or Testing the Code
1. Prerequisites
Install Python 3.x.
No external dependencies are required; the script uses Python’s built-in sqlite3, socket, and json libraries.
2. Running the Code
Save the script as merged_notes.py.
Run the script in a terminal or command prompt:

python merged_notes.py
Follow the on-screen menu to perform actions:
[1] Add Note → Enter a title and content.
[2] View Notes → Display all stored notes.
[3] Update Note → Modify an existing note by ID.
[4] Delete Note → Remove a note by ID.
[5] Exit → Quit the program.
3. Example Usage

Options: [1] Add Note  [2] View Notes  [3] Update Note  [4] Delete Note  [5] Exit
Choose an option: 1
Enter note title: Meeting Notes
Enter note content: Discussed project deadlines
{'message': 'Note added successfully'}

Choose an option: 2
Notes:
[1] Meeting Notes - Discussed project deadlines

Choose an option: 3
Enter note ID to update: 1
Enter new title: Updated Meeting Notes
Enter new content: Discussed project and assigned tasks
{'message': 'Note updated successfully'}

Choose an option: 4
Enter note ID to delete: 1
{'message': 'Note deleted successfully'}
Relevant Details About the Project
Architecture:

Two-Tier Architecture → Merged Server and Client into one script.
Server runs in the background and listens for client requests.
Client sends CRUD operations using TCP communication.
Key Features:

Uses SQLite as the database for persistent storage.
Multi-threaded server runs in parallel with the client.
Easy-to-use CLI menu for interacting with notes.
This project demonstrates how a database-driven application can be structured in a two-tier model, where the server manages the database, and the client communicates through network requests. 
