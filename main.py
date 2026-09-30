"""Main CLI application interface for Student Tracker."""

import os
import sys
from student import Student
from tracker import StudentTracker


def print_menu():
    print("\n" + "=" * 40)
    print("        STUDENT TRACKER SYSTEM        ")
    print("=" * 40)
    print("1. Add Student")
    print("2. Remove Student")
    print("3. Add/Update Grade for Student")
    print("4. View Student Details")
    print("5. List All Students")
    print("6. Search Student by Name")
    print("7. View Class Statistics")
    print("8. Save Data to JSON File")
    print("9. Load Data from JSON File")
    print("0. Exit")
    print("=" * 40)


def add_student_ui(tracker: StudentTracker):
    student_id = input("Enter Student ID: ").strip()
    if not student_id:
        print("Error: Student ID cannot be empty.")
        return
    name = input("Enter Student Name: ").strip()
    if not name:
        print("Error: Student Name cannot be empty.")
        return

    try:
        student = Student(student_id, name)
        tracker.add_student(student)
        print(f"Successfully added student '{name}' (ID: {student_id}).")
    except ValueError as e:
        print(f"Error: {e}")


def remove_student_ui(tracker: StudentTracker):
    student_id = input("Enter Student ID to remove: ").strip()
    if tracker.remove_student(student_id):
        print(f"Student with ID '{student_id}' has been removed.")
    else:
        print(f"Error: Student with ID '{student_id}' not found.")


def add_grade_ui(tracker: StudentTracker):
    student_id = input("Enter Student ID: ").strip()
    student = tracker.get_student(student_id)
    if not student:
        print(f"Error: Student with ID '{student_id}' not found.")
        return

    course = input("Enter Course Name: ").strip()
    try:
        grade = float(input("Enter Grade (0-100): ").strip())
        student.add_grade(course, grade)
        print(f"Grade {grade} added/updated for course '{course}' (Student: {student.name}).")
    except ValueError as e:
        print(f"Error: Invalid input or grade value ({e}).")


def view_student_ui(tracker: StudentTracker):
    student_id = input("Enter Student ID: ").strip()
    student = tracker.get_student(student_id)
    if not student:
        print(f"Error: Student with ID '{student_id}' not found.")
        return

    print("\n--- Student Information ---")
    print(f"ID: {student.student_id}")
    print(f"Name: {student.name}")
    print("Grades:")
    if student.grades:
        for course, grade in student.grades.items():
            print(f"  - {course}: {grade:.2f}")
        print(f"Average Grade: {student.get_average_grade():.2f}")
    else:
        print("  No grades recorded yet.")


def list_students_ui(tracker: StudentTracker):
    students = tracker.get_all_students()
    if not students:
        print("No students registered in the tracker.")
        return

    print("\n--- List of Students ---")
    for s in students:
        print(s)


def search_student_ui(tracker: StudentTracker):
    query = input("Enter student name or part of name to search: ").strip()
    results = tracker.search_by_name(query)
    if not results:
        print("No matching students found.")
        return

    print(f"\n--- Found {len(results)} Student(s) ---")
    for s in results:
        print(s)


def view_class_stats_ui(tracker: StudentTracker):
    students = tracker.get_all_students()
    total_students = len(students)
    if total_students == 0:
        print("No students in the tracker to calculate statistics.")
        return

    class_avg = tracker.calculate_class_average()
    print("\n--- Class Statistics ---")
    print(f"Total Students: {total_students}")
    print(f"Overall Class Average Grade: {class_avg:.2f}")


def save_data_ui(tracker: StudentTracker):
    filepath = input("Enter filename to save data (default: students.json): ").strip()
    if not filepath:
        filepath = "students.json"

    try:
        tracker.save_to_json(filepath)
        print(f"Data successfully saved to '{filepath}'.")
    except Exception as e:
        print(f"Error saving data: {e}")


def load_data_ui(tracker: StudentTracker):
    filepath = input("Enter filename to load data from (default: students.json): ").strip()
    if not filepath:
        filepath = "students.json"

    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' does not exist.")
        return

    try:
        tracker.load_from_json(filepath)
        print(f"Data successfully loaded from '{filepath}'. Total students: {len(tracker.students)}")
    except Exception as e:
        print(f"Error loading data: {e}")


def main():
    tracker = StudentTracker()

    # Auto load students.json if it exists
    if os.path.exists("students.json"):
        try:
            tracker.load_from_json("students.json")
            print("Loaded existing student data from 'students.json'.")
        except Exception:
            pass

    while True:
        print_menu()
        choice = input("Enter your choice (0-9): ").strip()

        if choice == "1":
            add_student_ui(tracker)
        elif choice == "2":
            remove_student_ui(tracker)
        elif choice == "3":
            add_grade_ui(tracker)
        elif choice == "4":
            view_student_ui(tracker)
        elif choice == "5":
            list_students_ui(tracker)
        elif choice == "6":
            search_student_ui(tracker)
        elif choice == "7":
            view_class_stats_ui(tracker)
        elif choice == "8":
            save_data_ui(tracker)
        elif choice == "9":
            load_data_ui(tracker)
        elif choice == "0":
            print("Exiting Student Tracker. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option. Please enter a number between 0 and 9.")


if __name__ == "__main__":
    main()
