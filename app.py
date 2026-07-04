from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"classes": [], "assignments": [], "marks": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# ============= HOME PAGE =============
@app.route('/')
def home():
    data = load_data()
    return render_template('index.html', 
                         classes_count=len(data['classes']),
                         assignments_count=len(data['assignments']),
                         marks_count=len(data['marks']))

# ============= CLASSES ROUTES =============
@app.route('/classes')
def classes():
    data = load_data()
    return render_template('classes.html', classes=data['classes'])

@app.route('/api/classes', methods=['POST'])
def add_class():
    data = load_data()
    class_info = {
        "id": len(data["classes"]) + 1,
        "subject": request.form['subject'],
        "professor": request.form['professor'],
        "timing": request.form['timing'],
        "room": request.form['room'],
        "created_date": datetime.now().strftime("%Y-%m-%d")
    }
    data["classes"].append(class_info)
    save_data(data)
    return redirect(url_for('classes'))

@app.route('/api/classes/delete/<int:class_id>', methods=['GET'])
def delete_class(class_id):
    data = load_data()
    data["classes"] = [c for c in data["classes"] if c["id"] != class_id]
    save_data(data)
    return redirect(url_for('classes'))

# ============= ASSIGNMENTS ROUTES =============
@app.route('/assignments')
def assignments():
    data = load_data()
    return render_template('assignments.html', assignments=data['assignments'])

@app.route('/api/assignments', methods=['POST'])
def add_assignment():
    data = load_data()
    asg_info = {
        "id": len(data["assignments"]) + 1,
        "subject": request.form['subject'],
        "assignment": request.form['assignment'],
        "deadline": request.form['deadline'],
        "completed": False,
        "created_date": datetime.now().strftime("%Y-%m-%d")
    }
    data["assignments"].append(asg_info)
    save_data(data)
    return redirect(url_for('assignments'))

@app.route('/api/assignments/complete/<int:asg_id>', methods=['GET'])
def complete_assignment(asg_id):
    data = load_data()
    for asg in data["assignments"]:
        if asg["id"] == asg_id:
            asg["completed"] = True
    save_data(data)
    return redirect(url_for('assignments'))

@app.route('/api/assignments/delete/<int:asg_id>', methods=['GET'])
def delete_assignment(asg_id):
    data = load_data()
    data["assignments"] = [a for a in data["assignments"] if a["id"] != asg_id]
    save_data(data)
    return redirect(url_for('assignments'))

# ============= MARKS ROUTES =============
@app.route('/marks')
def marks():
    data = load_data()
    return render_template('marks.html', marks=data['marks'])

@app.route('/api/marks', methods=['POST'])
def add_marks():
    data = load_data()
    marks_obtained = float(request.form['marks'])
    total_marks = float(request.form['total_marks'])
    percentage = (marks_obtained / total_marks) * 100
    
    mark_info = {
        "id": len(data["marks"]) + 1,
        "subject": request.form['subject'],
        "marks": marks_obtained,
        "total_marks": total_marks,
        "percentage": percentage,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    data["marks"].append(mark_info)
    save_data(data)
    return redirect(url_for('marks'))

@app.route('/api/marks/delete/<int:mark_id>', methods=['GET'])
def delete_marks(mark_id):
    data = load_data()
    data["marks"] = [m for m in data["marks"] if m["id"] != mark_id]
    save_data(data)
    return redirect(url_for('marks'))

# ============= DASHBOARD ROUTE =============
@app.route('/dashboard')
def dashboard():
    data = load_data()
    
    # Calculate stats
    total_assignments = len(data['assignments'])
    completed_assignments = len([a for a in data['assignments'] if a['completed']])
    pending_assignments = total_assignments - completed_assignments
    
    avg_percentage = 0
    if data['marks']:
        avg_percentage = sum(m['percentage'] for m in data['marks']) / len(data['marks'])
    
    # Calculate GPA
    if avg_percentage >= 90:
        gpa = 4.0
        grade = "A+"
    elif avg_percentage >= 80:
        gpa = 3.5
        grade = "A"
    elif avg_percentage >= 70:
        gpa = 3.0
        grade = "B"
    elif avg_percentage >= 60:
        gpa = 2.5
        grade = "C"
    else:
        gpa = 2.0
        grade = "D"
    
    return render_template('dashboard.html',
                         classes_count=len(data['classes']),
                         assignments_count=total_assignments,
                         completed_assignments=completed_assignments,
                         pending_assignments=pending_assignments,
                         marks_count=len(data['marks']),
                         avg_percentage=avg_percentage,
                         gpa=gpa,
                         grade=grade)

if __name__ == '__main__':
    app.run(debug=True, port=5000)