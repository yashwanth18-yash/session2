"""StudentTracker class managing a collection of students and persistence."""

import json
from typing import Dict, List, Optional
from student import Student


class StudentTracker:
    """Manages students and provides utility methods for analytics and storage."""

    def __init__(self):
        self.students: Dict[str, Student] = {}

    def add_student(self, student: Student) -> None:
        """Add a student to the tracker. Raises ValueError if student_id exists."""
        if not student.student_id:
            raise ValueError("Student ID cannot be empty.")
        if student.student_id in self.students:
            raise ValueError(f"Student with ID '{student.student_id}' already exists.")
        self.students[student.student_id] = student

    def remove_student(self, student_id: str) -> bool:
        """Remove a student by ID. Returns True if removed, False if not found."""
        student_id_clean = str(student_id).strip()
        if student_id_clean in self.students:
            del self.students[student_id_clean]
            return True
        return False

    def get_student(self, student_id: str) -> Optional[Student]:
        """Get student by ID."""
        return self.students.get(str(student_id).strip())

    def search_by_name(self, name_query: str) -> List[Student]:
        """Search students by name (case-insensitive substring match)."""
        query = name_query.strip().lower()
        if not query:
            return []
        return [
            s for s in self.students.values() if query in s.name.lower()
        ]

    def calculate_class_average(self) -> float:
        """Calculate overall average grade across all students and all courses."""
        all_grades = []
        for student in self.students.values():
            all_grades.extend(student.grades.values())
        if not all_grades:
            return 0.0
        return sum(all_grades) / len(all_grades)

    def get_all_students(self) -> List[Student]:
        """Return list of all students sorted by student_id."""
        return sorted(self.students.values(), key=lambda s: s.student_id)

    def save_to_json(self, filepath: str) -> None:
        """Save student records to a JSON file."""
        data = {
            student_id: student.to_dict()
            for student_id, student in self.students.items()
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_from_json(self, filepath: str) -> None:
        """Load student records from a JSON file."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.students.clear()
        for student_id, student_data in data.items():
            self.students[student_id] = Student.from_dict(student_data)
