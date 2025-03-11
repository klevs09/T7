Details About the Project's Database Architecture
1. Single-Tier Architecture:
In a single-tier architecture, the database and the application (or client) exist in the same environment. The client directly interacts with the database without a middleman or server. Examples include local database applications where everything runs on the same machine (e.g., SQLite in a desktop application).
Advantage: Simplified design, fast access.
Disadvantage: Limited scalability and security.
2. Two-Tier Architecture:
The current project follows a two-tier architecture, where there are two layers:
Client (Tier 1): The user interacts with a Python interface that sends requests for CRUD operations.
Server (Tier 2): The server handles the database (SQLite) and processes the client’s requests.
Communication: The client and server communicate over a network using TCP (Transmission Control Protocol).
Advantage: Separation of concerns, the client does not need to directly access the database, making the system more secure and easier to scale.
Disadvantage: Limited to direct client-server interactions. Multiple clients can interact with the server, but scalability is limited compared to a multi-tier architecture.
3. Three-Tier Architecture:
In a three-tier architecture, there are three layers:
Presentation Layer (Client): The user interface that interacts with the middle layer.
Logic/Business Layer (Server): Contains the logic or rules of how data can be accessed or modified. It acts as an intermediary between the client and the database.
Data Layer (Database): Stores the actual data (e.g., using a DBMS like MySQL, PostgreSQL).
Advantage: Increased scalability, flexibility, and separation of concerns. It supports more users and allows for better load balancing.
Disadvantage: More complex to implement and maintain compared to single or two-tier architectures.
Conclusion:
This project demonstrates a two-tier architecture where the client and server are distinct entities. The server handles database management with SQLite, while the client sends TCP requests to interact with it. This architecture is appropriate for small-scale applications and allows for clear separation between the database operations and the user-facing client.
