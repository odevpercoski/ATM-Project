# ATM System Control - Backend Simulation

This repository contains the implementation of a banking automation (ATM) system developed in Python. The main focus of the project was the application of **Separation of Concerns (SoC)** principles, data persistence via file systems, and robustness in input validation.

## 🛠 Architecture and Technical Decisions

The project was structured in a modular way to ensure maintainability and facilitate future migrations to frameworks or relational databases.

- **State Persistence:** Implementation of persistence via JSON, simulating a NoSQL database for storing user profiles, transaction histories, and session metadata.
- **Data Validation & Security:** Implementation of input sanitization logic (Regex-like logic) for CPF numbers (Brazilian tax identification numbers), names, and passwords, in addition to state control for failed authentication attempts.
- **Business Logic:** Centralization of business rules (score calculation, withdrawal/deposit logic, and statement update) in modules isolated from terminal I/O functions.
- **UX via CLI:** Development of a command-line interface with synchronous flow control and real-time feedback.

## 📊 Data Structure (Schema)
The system operates with a structured JSON object to support horizontal scalability of attributes, including:
- `account_balance`: Financial integrity control.
- `account_score`: Engagement algorithm based on transactional volume.
- `account_statement`: Chronological log of events for user auditing.

## 🚀 Installation and Execution

```bash
# Clone the repository
git clone [https://github.com/odevpercoski/ATM-Project](https://github.com/odevpercoski/ATM-Project)

# Execute the system entry point
python account_login.py
