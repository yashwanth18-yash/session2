"""Unit tests for Student and StudentTracker classes."""

import os
import pytest
from student import Student
from tracker import StudentTracker


class TestStudent:
    def test_student_initialization(self):
        s = Student("S101", "Alice Smith")
        assert s.student_id == "S101"
        assert s.name == "Alice Smith"
        assert s.grades == {}

    def test_add_grade_valid(self):
        s = Student("S101", "Alice Smith")
        s.add_grade("Math", 95.5)
        s.add_grade("English", 88.0)
        assert s.grades["Math"] == 95.5
        assert s.grades["English"] == 88.0

    def test_add_grade_invalid_course(self):
        s = Student("S101", "Alice Smith")
        with pytest.raises(ValueError, match="Course name cannot be empty"):
            s.add_grade("", 90)

    def test_add_grade_invalid_score(self):
        s = Student("S101", "Alice Smith")
        with pytest.raises(ValueError, match="Grade must be between 0 and 100"):
            s.add_grade("Math", -5)
        with pytest.raises(ValueError, match="Grade must be between 0 and 100"):
            s.add_grade("Math", 105)

    def test_get_average_grade(self):
        s = Student("S101", "Alice Smith")
        assert s.get_average_grade() == 0.0
        s.add_grade("Math", 90.0)
        s.add_grade("English", 80.0)
        assert s.get_average_grade() == 85.0

    def test_to_dict_and_from_dict(self):
        s = Student("S101", "Alice Smith", {"Math": 90.0, "Science": 95.0})
        data = s.to_dict()
        assert data == {
            "student_id": "S101",
            "name": "Alice Smith",
            "grades": {"Math": 90.0, "Science": 95.0},
        }

        s2 = Student.from_dict(data)
        assert s2.student_id == "S101"
        assert s2.name == "Alice Smith"
        assert s2.grades == {"Math": 90.0, "Science": 95.0}


class TestStudentTracker:
    def test_add_student(self):
        tracker = StudentTracker()
        s = Student("S101", "Alice")
        tracker.add_student(s)
        assert tracker.get_student("S101") == s

    def test_add_duplicate_student_raises_error(self):
        tracker = StudentTracker()
        s1 = Student("S101", "Alice")
        s2 = Student("S101", "Bob")
        tracker.add_student(s1)
        with pytest.raises(ValueError, match="already exists"):
            tracker.add_student(s2)

    def test_remove_student(self):
        tracker = StudentTracker()
        s = Student("S101", "Alice")
        tracker.add_student(s)
        assert tracker.remove_student("S101") is True
        assert tracker.get_student("S101") is None
        assert tracker.remove_student("S101") is False

    def test_search_by_name(self):
        tracker = StudentTracker()
        s1 = Student("S101", "Alice Smith")
        s2 = Student("S102", "Bob Johnson")
        s3 = Student("S103", "Alice Cooper")
        tracker.add_student(s1)
        tracker.add_student(s2)
        tracker.add_student(s3)

        results = tracker.search_by_name("alice")
        assert len(results) == 2
        assert s1 in results and s3 in results

    def test_class_average(self):
        tracker = StudentTracker()
        assert tracker.calculate_class_average() == 0.0

        s1 = Student("S101", "Alice", {"Math": 100.0, "Science": 80.0})
        s2 = Student("S102", "Bob", {"Math": 60.0})
        tracker.add_student(s1)
        tracker.add_student(s2)

        # Total grades: 100 + 80 + 60 = 240. Count: 3. Average = 80.0
        assert tracker.calculate_class_average() == 80.0

    def test_save_and_load_json(self, tmp_path):
        filepath = os.path.join(tmp_path, "test_students.json")
        tracker = StudentTracker()
        s1 = Student("S101", "Alice", {"Math": 90.0})
        s2 = Student("S102", "Bob", {"History": 85.0})
        tracker.add_student(s1)
        tracker.add_student(s2)

        tracker.save_to_json(filepath)
        assert os.path.exists(filepath)

        new_tracker = StudentTracker()
        new_tracker.load_from_json(filepath)
        assert len(new_tracker.students) == 2
        loaded_s1 = new_tracker.get_student("S101")
        assert loaded_s1 is not None
        assert loaded_s1.name == "Alice"
        assert loaded_s1.grades == {"Math": 90.0}
