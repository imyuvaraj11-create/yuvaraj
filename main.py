import json
import os
from datetime import datetime

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"classes": [], "assignments": [], "marks": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_class(data):
    print("\n--- Add New Class ---")
    subject = input("Subject Name: ").strip()
    professor = input("Professor Name: ").strip()
    timing = input("Class Timing: ").strip()
    room = input("Room Number: ").strip()
    
    class_info = {"subject": subject, "professor": professor, "timing": timing, "room": room}
    data["classes"].append(class_info)
    save_data(data)
    print("✅ Class added!")

def view_classes(data):
    print("\n--- Your Classes ---")
    if not data["classes"]:
        print("No classes yet!")
        return
    for i, cls in enumerate(data["classes"], 1):
        print(f"\n{i}. {cls['subject']}")
        print(f"   Professor: {cls['professor']}")
        print(f"   Time: {cls['timing']}")
        print(f"   Room: {cls['room']}")

def add_assignment(data):
    print("\n--- Add Assignment ---")
    subject = input("Subject Name: ").strip()
    assignment = input("Assignment Description: ").strip()
    deadline = input("Deadline (YYYY-MM-DD): ").strip()
    
    asg_info = {"subject": subject, "assignment": assignment, "deadline": deadline, "completed": False}
    data["assignments"].append(asg_info)
    save_data(data)
    print("✅ Assignment added!")

def view_assignments(data):
    print("\n--- Your Assignments ---")
    if not data["assignments"]:
        print("No assignments yet!")
        return
    for i, asg in enumerate(data["assignments"], 1):
        status = "✅ Done" if asg["completed"] else "⏳ Pending"
        print(f"\n{i}. {asg['subject']}")
        print(f"   Task: {asg['assignment']}")
        print(f"   Deadline: {asg['deadline']}")
        print(f"   Status: {status}")

def mark_assignment_complete(data):
    print("\n--- Mark Complete ---")
    view_assignments(data)
    if not data["assignments"]:
        return
    try:
        idx = int(input("\nEnter assignment number: ")) - 1
        if 0 <= idx < len(data["assignments"]):
            data["assignments"][idx]["completed"] = True
            save_data(data)
            print("✅ Marked complete!")
        else:
            print("❌ Invalid number!")
    except ValueError:
        print("❌ Please enter a valid number!")

def add_marks(data):
    print("\n--- Add Marks ---")
    subject = input("Subject Name: ").strip()
    marks = float(input("Marks Obtained: "))
    total_marks = float(input("Total Marks: "))
    
    mark_info = {
        "subject": subject,
        "marks": marks,
        "total_marks": total_marks,
        "percentage": (marks / total_marks) * 100,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    data["marks"].append(mark_info)
    save_data(data)
    print("✅ Marks added!")

def view_marks(data):
    print("\n--- Your Marks ---")
    if not data["marks"]:
        print("No marks yet!")
        return
    for i, mark in enumerate(data["marks"], 1):
        print(f"\n{i}. {mark['subject']}")
        print(f"   Marks: {mark['marks']}/{mark['total_marks']}")
        print(f"   Percentage: {mark['percentage']:.2f}%")
        print(f"   Date: {mark['date']}")

def calculate_gpa(data):
    print("\n--- Calculate GPA ---")
    if not data["marks"]:
        print("No marks yet!")
        return
    
    total_percentage = sum(mark["percentage"] for mark in data["marks"])
    avg = total_percentage / len(data["marks"])
    
    if avg >= 90:
        gpa = 4.0
    elif avg >= 80:
        gpa = 3.5
    elif avg >= 70:
        gpa = 3.0
    elif avg >= 60:
        gpa = 2.5
    else:
        gpa = 2.0
    
    print(f"\nAverage: {avg:.2f}%")
    print(f"GPA: {gpa:.2f}")

def display_menu():
    print("\n" + "="*40)
    print("     🎓 CAMPUS BUDDY 🎓")
    print("="*40)
    print("1. Add Class")
    print("2. View Classes")
    print("3. Add Assignment")
    print("4. View Assignments")
    print("5. Mark Complete")
    print("6. Add Marks")
    print("7. View Marks")
    print("8. Calculate GPA")
    print("9. Exit")
    print("="*40)

def main():
    print("\n🎓 Welcome to Campus Buddy! 🎓\n")
    
    while True:
        data = load_data()
        display_menu()
        choice = input("\nEnter choice (1-9): ").strip()
        
        if choice == "1":
            add_class(data)
        elif choice == "2":
            view_classes(data)
        elif choice == "3":
            add_assignment(data)
        elif choice == "4":
            view_assignments(data)
        elif choice == "5":
            mark_assignment_complete(data)
        elif choice == "6":
            add_marks(data)
        elif choice == "7":
            view_marks(data)
        elif choice == "8":
            calculate_gpa(data)
        elif choice == "9":
            print("\n👋 Goodbye! Good luck with studies! 🚀\n")
            break
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()