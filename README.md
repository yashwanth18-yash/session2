# Student Tracker in Python

A simple, lightweight, and interactive command-line Student Tracker written in Python. This application allows users to manage student records, record course grades, search students, calculate individual and class statistics, and persist data using JSON files.

## Features

- **Student Management**: Add, remove, and retrieve student records by unique Student ID.
- **Grade Tracking**: Add or update numerical course grades (0-100) for any student.
- **Analytics & Statistics**:
  - Calculate individual student average grades.
  - Calculate overall class average grades across all courses and students.
- **Search Capabilities**: Case-insensitive search by student name or substring.
- **Data Persistence**: Save and load student records to/from JSON files (default: `students.json`).

## Project Structure

```text
.
├── student.py           # Core Student class and grade management
├── tracker.py           # StudentTracker class for student collection and persistence
├── main.py              # Interactive CLI menu application
├── tests/
│   └── test_tracker.py  # Automated unit tests using pytest
└── README.md            # Project documentation
```

## Setup & Running

### Requirements
- Python 3.8+
- `pytest` (for running tests)

### Running the CLI Application

To launch the interactive CLI application:

```bash
python3 main.py
```

### Running Tests

To run the automated pytest test suite:

```bash
PYTHONPATH=. pytest
```
