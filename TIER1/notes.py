import sqlite3

DB_FILE = "notes.db"

# Initialize the database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Add a new note
def add_note(title, content):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()
    print(f"Note '{title}' added successfully!")

# Delete a note by ID
def delete_note(note_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    print(f"Note ID {note_id} deleted successfully!")

# View all notes
def view_notes():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    conn.close()

    if not notes:
        print("No notes found.")
    else:
        print("\nAll Notes:")
        for note in notes:
            print(f"[{note[0]}] {note[1]} - {note[2]}")

# CLI Interface
def main():
    init_db()
    
    while True:
        print("\nOptions: [1] Add Note  [2] View Notes  [3] Delete Note  [4] Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Enter note title: ")
            content = input("Enter note content: ")
            add_note(title, content)

        elif choice == "2":
            view_notes()

        elif choice == "3":
            note_id = input("Enter note ID to delete: ")
            if note_id.isdigit():
                delete_note(int(note_id))
            else:
                print("Invalid ID!")

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
