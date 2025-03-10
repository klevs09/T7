document.addEventListener("DOMContentLoaded", fetchNotes);

function fetchNotes() {
    fetch("/notes")
        .then(response => response.json())
        .then(notes => {
            const notesList = document.getElementById("notes-list");
            notesList.innerHTML = "";
            notes.forEach(note => {
                notesList.innerHTML += `
                    <div class="note">
                        <h3>${note.title}</h3>
                        <p>${note.content}</p>
                        <button onclick="updateNote(${note.id})">Update</button>
                        <button onclick="deleteNote(${note.id})">Delete</button>
                    </div>
                `;
            });
        });
}

function addNote() {
    const title = document.getElementById("title").value;
    const content = document.getElementById("content").value;

    fetch("/add_note", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, content })
    })
    .then(() => {
        document.getElementById("title").value = "";
        document.getElementById("content").value = "";
        fetchNotes();
    });
}

function deleteNote(id) {
    fetch(`/delete_note?id=${id}`, { method: "DELETE" })
        .then(() => fetchNotes());
}

function updateNote(id) {
    const newTitle = prompt("Enter new title:");
    const newContent = prompt("Enter new content:");

    fetch("/update_note", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, title: newTitle, content: newContent })
    })
    .then(() => fetchNotes());
}
