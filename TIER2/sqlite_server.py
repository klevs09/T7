import sqlite3
import json
import socket
import threading

DB_FILE = "notes.db"
HOST = "127.0.0.1"
PORT = 5000

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

# Handle CRUD operations
def handle_request(request):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    request = json.loads(request)
    action = request.get("action")

    if action == "create":
        cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", 
                       (request["title"], request["content"]))
        conn.commit()
        response = {"message": "Note added successfully"}

    elif action == "read":
        cursor.execute("SELECT * FROM notes")
        notes = [{"id": row[0], "title": row[1], "content": row[2]} for row in cursor.fetchall()]
        response = notes

    elif action == "update":
        cursor.execute("UPDATE notes SET title=?, content=? WHERE id=?", 
                       (request["title"], request["content"], request["id"]))
        conn.commit()
        response = {"message": "Note updated successfully"}

    elif action == "delete":
        cursor.execute("DELETE FROM notes WHERE id=?", (request["id"],))
        conn.commit()
        response = {"message": "Note deleted successfully"}

    else:
        response = {"error": "Invalid action"}

    conn.close()
    return json.dumps(response)

# Server function to listen for requests
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Server running on {HOST}:{PORT}")

        while True:
            client, addr = server.accept()
            with client:
                data = client.recv(1024)
                if data:
                    response = handle_request(data.decode())
                    client.sendall(response.encode())

# Start the server in a separate thread
def start_server_thread():
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

# Client function to send requests to the server
def send_request(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        client.sendall(json.dumps(data).encode())
        response = client.recv(4096).decode()
        return json.loads(response)

# Client-side CRUD operations
def add_note(title, content):
    request = {"action": "create", "title": title, "content": content}
    print(send_request(request))

def view_notes():
    request = {"action": "read"}
    response = send_request(request)
    if response:
        print("\nNotes:")
        for note in response:
            print(f"[{note['id']}] {note['title']} - {note['content']}")
    else:
        print("No notes found.")

def update_note(note_id, title, content):
    request = {"action": "update", "id": note_id, "title": title, "content": content}
    print(send_request(request))

def delete_note(note_id):
    request = {"action": "delete", "id": note_id}
    print(send_request(request))

# CLI Interface for interaction
def main():
    init_db()
    start_server_thread()

    while True:
        print("\nOptions: [1] Add Note  [2] View Notes  [3] Update Note  [4] Delete Note  [5] Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Enter note title: ")
            content = input("Enter note content: ")
            add_note(title, content)

        elif choice == "2":
            view_notes()

        elif choice == "3":
            note_id = input("Enter note ID to update: ")
            title = input("Enter new title: ")
            content = input("Enter new content: ")
            update_note(int(note_id), title, content)

        elif choice == "4":
            note_id = input("Enter note ID to delete: ")
            delete_note(int(note_id))

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
