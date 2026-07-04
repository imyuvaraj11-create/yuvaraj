import json
import os
from datetime import datetime
from pathlib import Path

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"classes": [], "assignments": [], "marks": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# ============= CLASS FUNCTIONS =============

def add_class(data):
    print("\n--- Add New Class ---")
    subject = input("Subject Name: ").strip()
    professor = input("Professor Name: ").strip()
    timing = input("Class Timing: ").strip()
    room = input("Room Number: ").strip()
    
    class_info = {
        "id": len(data["classes"]) + 1,
        "subject": subject,
        "professor": professor,
        "timing": timing,
        "room": room,
        "created_date": datetime.now().strftime("%Y-%m-%d")
    }
    
    data["classes"].append(class_info)
    save_data(data)
    print("✅ Class added successfully!")

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

def search_class(data):
    print("\n--- Search Class ---")
    search_term = input("Enter subject name to search: ").strip().lower()
    found = [cls for cls in data["classes"] if search_term in cls['subject'].lower()]
    
    if not found:
        print(f"❌ No classes found with '{search_term}'")
        return
    
    print(f"\n✅ Found {len(found)} class(es):")
    for i, cls in enumerate(found, 1):
        print(f"\n{i}. {cls['subject']}")
        print(f"   Professor: {cls['professor']}")
        print(f"   Time: {cls['timing']}")
        print(f"   Room: {cls['room']}")

def edit_class(data):
    print("\n--- Edit Class ---")
    view_classes(data)
    
    if not data["classes"]:
        return
    
    try:
        idx = int(input("\nEnter class number to edit: ")) - 1
        if 0 <= idx < len(data["classes"]):
            cls = data["classes"][idx]
            print(f"\nEditing: {cls['subject']}")
            print("Leave blank to keep current value")
            
            new_subject = input(f"Subject ({cls['subject']}): ").strip() or cls['subject']
            new_professor = input(f"Professor ({cls['professor']}): ").strip() or cls['professor']
            new_timing = input(f"Timing ({cls['timing']}): ").strip() or cls['timing']
            new_room = input(f"Room ({cls['room']}): ").strip() or cls['room']
            
            data["classes"][idx] = {
                "id": cls["id"],
                "subject": new_subject,
                "professor": new_professor,
                "timing": new_timing,
                "room": new_room,
                "created_date": cls["created_date"]
            }
            save_data(data)
            print("✅ Class updated!")
        else:
            print("❌ Invalid class number!")
    except ValueError:
        print("❌ Please enter a valid number!")

def delete_class(data):
    print("\n--- Delete Class ---")
    view_classes(data)
    
    if not data["classes"]:
        return
    
    try:
        idx = int(input("\nEnter class number to delete: ")) - 1
        if 0 <= idx < len(data["classes"]):
            deleted = data["classes"].pop(idx)
            save_data(data)
            print(f"✅ Deleted: {deleted['subject']}")
        else:
            print("❌ Invalid class number!")
    except ValueError:
        print("❌ Please enter a valid number!")

# ============= ASSIGNMENT FUNCTIONS =============

def add_assignment(data):
    print("\n--- Add Assignment ---")
    subject = input("Subject Name: ").strip()
    assignment = input("Assignment Description: ").strip()
    deadline = input("Deadline (YYYY-MM-DD): ").strip()
    
    asg_info = {
        "id": len(data["assignments"]) + 1,
        "subject": subject,
        "assignment": assignment,
        "deadline": deadline,
        "completed": False,
        "created_date": datetime.now().strftime("%Y-%m-%d")
    }
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

def search_assignment(data):
    print("\n--- Search Assignment ---")
    search_term = input("Enter subject or assignment keyword: ").strip().lower()
    found = [asg for asg in data["assignments"] 
             if search_term in asg['subject'].lower() or search_term in asg['assignment'].lower()]
    
    if not found:
        print(f"❌ No assignments found with '{search_term}'")
        return
    
    print(f"\n✅ Found {len(found)} assignment(s):")
    for i, asg in enumerate(found, 1):
        status = "✅ Done" if asg["completed"] else "⏳ Pending"
        print(f"\n{i}. {asg['subject']}")
        print(f"   Task: {asg['assignment']}")
        print(f"   Deadline: {asg['deadline']}")
        print(f"   Status: {status}")

def sort_assignments(data):
    print("\n--- Sort Assignments ---")
    print("1. By Deadline (Earliest first)")
    print("2. By Status (Pending first)")
    choice = input("Enter choice (1-2): ").strip()
    
    if choice == "1":
        sorted_asg = sorted(data["assignments"], key=lambda x: x['deadline'])
        print("\n--- Sorted by Deadline ---")
    elif choice == "2":
        sorted_asg = sorted(data["assignments"], key=lambda x: x['completed'])
        print("\n--- Sorted by Status ---")
    else:
        print("❌ Invalid choice!")
        return
    
    for i, asg in enumerate(sorted_asg, 1):
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

def edit_assignment(data):
    print("\n--- Edit Assignment ---")
    view_assignments(data)
    
    if not data["assignments"]:
        return
    
    try:
        idx = int(input("\nEnter assignment number to edit: ")) - 1
        if 0 <= idx < len(data["assignments"]):
            asg = data["assignments"][idx]
            print(f"\nEditing: {asg['assignment']}")
            
            new_subject = input(f"Subject ({asg['subject']}): ").strip() or asg['subject']
            new_assignment = input(f"Assignment ({asg['assignment']}): ").strip() or asg['assignment']
            new_deadline = input(f"Deadline ({asg['deadline']}): ").strip() or asg['deadline']
            
            data["assignments"][idx] = {
                "id": asg["id"],
                "subject": new_subject,
                "assignment": new_assignment,
                "deadline": new_deadline,
                "completed": asg["completed"],
                "created_date": asg["created_date"]
            }
            save_data(data)
            print("✅ Assignment updated!")
        else:
            print("❌ Invalid assignment number!")
    except ValueError:
        print("❌ Please enter a valid number!")

def delete_assignment(data):
    print("\n--- Delete Assignment ---")
    view_assignments(data)
    
    if not data["assignments"]:
        return
    
    try:
        idx = int(input("\nEnter assignment number to delete: ")) - 1
        if 0 <= idx < len(data["assignments"]):
            deleted = data["assignments"].pop(idx)
            save_data(data)
            print(f"✅ Deleted: {deleted['assignment']}")
        else:
            print("❌ Invalid assignment number!")
    except ValueError:
        print("❌ Please enter a valid number!")

# ============= MARKS FUNCTIONS =============

def add_marks(data):
    print("\n--- Add Marks ---")
    subject = input("Subject Name: ").strip()
    marks = float(input("Marks Obtained: "))
    total_marks = float(input("Total Marks: "))
    
    mark_info = {
        "id": len(data["marks"]) + 1,
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
        grade = "A+"
    elif avg >= 80:
        gpa = 3.5
        grade = "A"
    elif avg >= 70:
        gpa = 3.0
        grade = "B"
    elif avg >= 60:
        gpa = 2.5
        grade = "C"
    else:
        gpa = 2.0
        grade = "D"
    
    print(f"\n{'='*40}")
    print(f"Average Percentage: {avg:.2f}%")
    print(f"GPA (4.0 scale): {gpa:.2f}")
    print(f"Grade: {grade}")
    print(f"{'='*40}")

def delete_marks(data):
    print("\n--- Delete Marks ---")
    view_marks(data)
    
    if not data["marks"]:
        return
    
    try:
        idx = int(input("\nEnter marks number to delete: ")) - 1
        if 0 <= idx < len(data["marks"]):
            deleted = data["marks"].pop(idx)
            save_data(data)
            print(f"✅ Deleted marks for: {deleted['subject']}")
        else:
            print("❌ Invalid marks number!")
    except ValueError:
        print("❌ Please enter a valid number!")

# ============= EXPORT FUNCTIONS =============

def export_to_file(data):
    print("\n--- Export Data ---")
    filename = f"campus_buddy_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    try:
        with open(filename, 'w') as f:
            f.write("="*50 + "\n")
            f.write("CAMPUS BUDDY - COMPLETE REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
            
            # Classes
            f.write("CLASSES\n")
            f.write("-"*50 + "\n")
            if data["classes"]:
                for cls in data["classes"]:
                    f.write(f"Subject: {cls['subject']}\n")
                    f.write(f"Professor: {cls['professor']}\n")
                    f.write(f"Timing: {cls['timing']}\n")
                    f.write(f"Room: {cls['room']}\n\n")
            else:
                f.write("No classes recorded.\n\n")
            
            # Assignments
            f.write("\nASSIGNMENTS\n")
            f.write("-"*50 + "\n")
            if data["assignments"]:
                for asg in data["assignments"]:
                    status = "COMPLETED" if asg["completed"] else "PENDING"
                    f.write(f"Subject: {asg['subject']}\n")
                    f.write(f"Task: {asg['assignment']}\n")
                    f.write(f"Deadline: {asg['deadline']}\n")
                    f.write(f"Status: {status}\n\n")
            else:
                f.write("No assignments recorded.\n\n")
            
            # Marks
            f.write("\nMARKS & GRADES\n")
            f.write("-"*50 + "\n")
            if data["marks"]:
                for mark in data["marks"]:
                    f.write(f"Subject: {mark['subject']}\n")
                    f.write(f"Marks: {mark['marks']}/{mark['total_marks']}\n")
                    f.write(f"Percentage: {mark['percentage']:.2f}%\n\n")
                
                # GPA Summary
                total_percentage = sum(mark["percentage"] for mark in data["marks"])
                avg = total_percentage / len(data["marks"])
                f.write(f"\nAverage Percentage: {avg:.2f}%\n")
                
                if avg >= 90:
                    gpa = 4.0
                    grade = "A+"
                elif avg >= 80:
                    gpa = 3.5
                    grade = "A"
                elif avg >= 70:
                    gpa = 3.0
                    grade = "B"
                elif avg >= 60:
                    gpa = 2.5
                    grade = "C"
                else:
                    gpa = 2.0
                    grade = "D"
                
                f.write(f"GPA (4.0 scale): {gpa:.2f}\n")
                f.write(f"Overall Grade: {grade}\n")
            else:
                f.write("No marks recorded.\n\n")
        
        print(f"✅ Data exported to: {filename}")
        print(f"📁 File saved in: {os.getcwd()}")
    except Exception as e:
        print(f"❌ Error exporting: {e}")

# ============= MENU =============

def display_menu():
    print("\n" + "="*50)
    print("🎓 CAMPUS BUDDY - ENHANCED VERSION 🎓")
    print("="*50)
    print("\n📚 CLASSES:")
    print("1. Add Class")
    print("2. View Classes")
    print("3. Search Class")
    print("4. Edit Class")
    print("5. Delete Class")
    print("\n📝 ASSIGNMENTS:")
    print("6. Add Assignment")
    print("7. View Assignments")
    print("8. Search Assignment")
    print("9. Sort Assignments")
    print("10. Mark Complete")
    print("11. Edit Assignment")
    print("12. Delete Assignment")
    print("\n📊 MARKS:")
    print("13. Add Marks")
    print("14. View Marks")
    print("15. Calculate GPA")
    print("16. Delete Marks")
    print("\n💾 EXPORT:")
    print("17. Export All Data")
    print("\n0. Exit")
    print("="*50)

def main():
    print("\n" + "="*50)
    print("🎓 Welcome to Campus Buddy Enhanced! 🎓")
    print("="*50)
    print("Your personal college management system!")
    print("="*50 + "\n")
    
    while True:
        data = load_data()
        display_menu()
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == "1":
            add_class(data)
        elif choice == "2":
            view_classes(data)
        elif choice == "3":
            search_class(data)
        elif choice == "4":
            edit_class(data)
        elif choice == "5":
            delete_class(data)
        elif choice == "6":
            add_assignment(data)
        elif choice == "7":
            view_assignments(data)
        elif choice == "8":
            search_assignment(data)
        elif choice == "9":
            sort_assignments(data)
        elif choice == "10":
            mark_assignment_complete(data)
        elif choice == "11":
            edit_assignment(data)
        elif choice == "12":
            delete_assignment(data)
        elif choice == "13":
            add_marks(data)
        elif choice == "14":
            view_marks(data)
        elif choice == "15":
            calculate_gpa(data)
        elif choice == "16":
            delete_marks(data)
        elif choice == "17":
            export_to_file(data)
        elif choice == "0":
            print("\n👋 Thanks for using Campus Buddy!")
            print("Good luck with your studies! 🚀\n")
            break
        else:
            print("❌ Invalid choice! Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()