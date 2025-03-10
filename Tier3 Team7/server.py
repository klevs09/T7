import http.server
import socketserver
import json
import sqlite3
from urllib.parse import urlparse, parse_qs

PORT = 8000
DB_FILE = "database.db"

# Initialize database
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

class NotesHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/notes":
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM notes")
            notes = [{"id": row[0], "title": row[1], "content": row[2]} for row in cursor.fetchall()]
            conn.close()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(notes).encode())

        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/add_note":
            content_length = int(self.headers["Content-Length"])
            post_data = json.loads(self.rfile.read(content_length))

            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", 
                           (post_data["title"], post_data["content"]))
            conn.commit()
            conn.close()

            self.send_response(201)
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Note added"}).encode())

    def do_DELETE(self):
        if self.path.startswith("/delete_note"):
            query = urlparse(self.path).query
            params = parse_qs(query)
            note_id = params.get("id", [None])[0]

            if note_id:
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
                conn.commit()
                conn.close()

                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Note deleted"}).encode())

    def do_PUT(self):
        if self.path.startswith("/update_note"):
            content_length = int(self.headers["Content-Length"])
            put_data = json.loads(self.rfile.read(content_length))

            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("UPDATE notes SET title=?, content=? WHERE id=?", 
                           (put_data["title"], put_data["content"], put_data["id"]))
            conn.commit()
            conn.close()

            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Note updated"}).encode())

if __name__ == "__main__":
    init_db()
    with socketserver.TCPServer(("", PORT), NotesHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()
