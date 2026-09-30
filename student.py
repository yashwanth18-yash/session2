"""Student class representing an individual student and their grades."""

from typing import Dict, Any


class Student:
    """Represents a student with an ID, name, and grades for courses."""

    def __init__(self, student_id: str, name: str, grades: Dict[str, float] = None):
        self.student_id = str(student_id).strip()
        self.name = str(name).strip()
        self.grades: Dict[str, float] = {}
        if grades:
            for course, grade in grades.items():
                self.add_grade(course, grade)

    def add_grade(self, course: str, grade: float) -> None:
        """Add or update a grade for a course."""
        course_clean = str(course).strip()
        if not course_clean:
            raise ValueError("Course name cannot be empty.")
        grade_val = float(grade)
        if grade_val < 0 or grade_val > 100:
            raise ValueError("Grade must be between 0 and 100.")
        self.grades[course_clean] = grade_val

    def get_average_grade(self) -> float:
        """Calculate and return the average grade of the student."""
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)

    def to_dict(self) -> Dict[str, Any]:
        """Convert student object to dictionary representation."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "grades": self.grades,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        """Create a Student instance from a dictionary."""
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            grades=data.get("grades", {}),
        )

    def __str__(self) -> str:
        avg = self.get_average_grade()
        return f"ID: {self.student_id} | Name: {self.name} | Courses: {len(self.grades)} | Average Grade: {avg:.2f}"
