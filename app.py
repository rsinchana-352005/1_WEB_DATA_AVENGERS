from flask import Flask, render_template, request
import sqlite3
from werkzeug.security import check_password_hash
from flask import flash, redirect, url_for


app = Flask(__name__)

# ---------------- HOME ---------------- #
app.secret_key = "secret123"
def calculate_grade(total):
    if total >= 90:
        return "o", 10
    elif total >= 80:
        return "A", 9
    elif total >= 70:
        return "B", 8
    elif total >= 60:
        return "C", 7
    elif total >= 50:
        return "D", 6
    else:
        return "F", 0
@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/roles')
def roles():
    return render_template('role_select.html')
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        return render_template('admin_dashboard.html')
    return render_template('login_admin.html')
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')
@app.route('/hod_dashboard')
def hod_dashboard():
    dept = request.args.get('dept')  # optional
    return render_template('hod_dashboard.html', dept=dept)
@app.route('/student_dashboard')
def student_dashboard():
    import sqlite3

    usn = request.args.get('usn')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM student WHERE usn=?", (usn,))
    user = cursor.fetchone()

    conn.close()

    return render_template('student_dashboard.html',
                           user=user,   
                           )
@app.route('/faculty_dashboard')
def faculty_dashboard():

    name = request.args.get('name')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT subject_code FROM faculty_assignment WHERE faculty_name=?", (name,))
    subjects = [row[0] for row in cursor.fetchall()]

    conn.close()

    return render_template('faculty_dashboard.html',
                           name=name,
                           subjects=subjects)

@app.route('/register_student', methods=['GET', 'POST'])
def register_student():
    import sqlite3
    from werkzeug.security import generate_password_hash

    if request.method == 'POST':
        name = request.form['name']
        usn = request.form['usn']
        dept = request.form['department']
        sem = request.form['semester']
        password = generate_password_hash(request.form['password'])

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO student (name, usn, department, semester, password)
        VALUES (?, ?, ?, ?, ?)
        ''', (name, usn, dept, sem, password))

        conn.commit()
        conn.close()

        flash("✅ Student Registered Successfully!")

        return redirect(url_for('register_student'))

    return render_template('register_student.html')

@app.route('/register_faculty', methods=['GET', 'POST'])
def register_faculty():
    import sqlite3

    if request.method == 'POST':
        name = request.form['name']
        dept = request.form['department']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO faculty (name, department, password)
        VALUES (?, ?, ?)
        ''', (name, dept, password))

        conn.commit()
        conn.close()

        flash("✅ Faculty Registered Successfully!")

        return redirect(url_for('register_faculty'))

    return render_template('register_faculty.html')

@app.route('/upload_results')
def upload_results():
    return render_template('upload.html')
# ---------------- STUDENT LOGIN ---------------- #

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        usn = request.form['usn']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM student WHERE usn=?", (usn,))
        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[5], password):

            # ✅ Get semester
            semester = int(user[4])

            # ✅ Subjects based on semester
            semester_subjects = {
                6: [
                    ("fsd", "Full Stack Development"),
                    ("ml", "Machine Learning"),
                    ("blockchain", "Blockchain Technology"),
                    ("oe", "Open Elective Course"),
                    ("project", "Project Phase I"),
                    ("ml_lab", "Machine Learning Lab"),
                    ("devops", "DevOps"),
                    ("fsd_lab", "Full Stack Development Lab")
                ]
            }

            subjects = semester_subjects.get(semester, [])

            return render_template('student_dashboard.html',
                                   user=user,
                                   subjects=subjects)

        else:
            return "Invalid Credentials"

    return render_template('login_student.html')


# ---------------- SUBJECT DETAILS ---------------- #

@app.route('/subject/<subject_name>')
def subject_details(subject_name):

    subject_map = {
        "fsd": ("Full Stack Development", "23CS601"),
        "ml": ("Machine Learning", "23CS602"),
        "blockchain": ("Blockchain Technology", "23CS603"),
        "oe": ("Open Elective Course", "23OE604"),
        "project": ("Project Phase I", "23CS605"),
        "ml_lab": ("Machine Learning Lab", "23CSL606"),
        "devops": ("DevOps", "23CS607"),
        "fsd_lab": ("Full Stack Development Lab", "23CSL608")
    }

    name, code = subject_map.get(subject_name, ("Unknown", ""))

    usn = request.args.get('usn')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT ia1, ia2, ia3, attendance
    FROM marks
    WHERE usn=? AND subject_code=?
    ''', (usn, code))

    row = cursor.fetchone()
    conn.close()

    if row:
        ia1, ia2, ia3, attendance = row
    else:
        ia1, ia2, ia3, attendance = 0, 0, 0, 0

    best_two = sorted([ia1, ia2, ia3], reverse=True)[:2]
    avg = sum(best_two) / 2

    return render_template('subject_details.html',
                           subject=name,
                           code=code,
                           ia1=ia1,
                           ia2=ia2,
                           ia3=ia3,
                           attendance=attendance,
                           avg=avg)
@app.route('/hod_login', methods=['GET', 'POST'])
def hod_login():
    if request.method == 'POST':
        dept = request.form['department']
        return render_template('hod_dashboard.html', dept=dept)

    return render_template('login_hod.html')


from flask import flash, redirect, url_for  # make sure already imported

@app.route('/hod_assign', methods=['GET', 'POST'])
def hod_assign():

    if request.method == 'POST':
        faculty_name = request.form['faculty_name']
        subject_code = request.form['subject_code']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO faculty_assignment (faculty_name, subject_code)
        VALUES (?, ?)
        ''', (faculty_name, subject_code))

        conn.commit()
        conn.close()

        flash("✅ Faculty Assigned Successfully!")

        return redirect(url_for('hod_assign'))

    return render_template('hod_assign.html')

@app.route('/hod_view')
def hod_view():
    import sqlite3

    dept = request.args.get('dept')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT s.usn, s.name, m.subject_code,
           m.ia1, m.ia2, m.ia3, m.attendance
    FROM student s
    JOIN marks m ON s.usn = m.usn
    WHERE s.department = ?
    ''', (dept,))

    rows = cursor.fetchall()
    conn.close()

    data = []

    for r in rows:
        best_two = sorted([r[3], r[4], r[5]], reverse=True)[:2]
        best_avg = sum(best_two) / 2

        data.append({
            "usn": r[0],
            "name": r[1],
            "subject": r[2],
            "ia1": r[3],
            "ia2": r[4],
            "ia3": r[5],
            "best": best_avg,
            "attendance": r[6],
            "sgpa": round(best_avg / 10, 2)
        })

    return render_template('hod_view.html', data=data)
@app.route('/hod_results')
def hod_results():
    import sqlite3

    dept = request.args.get('dept')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT s.usn, s.name,
           r.subject_code, r.credits,
           r.ia_total, r.see_marks,
           r.total, r.grade
    FROM student s
    JOIN results r ON s.usn = r.usn
    WHERE s.department = ?
    ORDER BY s.usn
    ''', (dept,))

    data = cursor.fetchall()
    conn.close()

    return render_template('hod_results.html',
                           data=data,
                           dept=dept)
# ---------------- FACULTY LOGIN ---------------- #

@app.route('/faculty_login', methods=['GET', 'POST'])
def faculty_login():
    import sqlite3

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM faculty WHERE name=? AND password=?", (name, password))
        user = cursor.fetchone()

        if user:
            cursor.execute("SELECT subject_code FROM faculty_assignment WHERE faculty_name=?", (name,))
            subjects = [row[0] for row in cursor.fetchall()]

            conn.close()

            return render_template('faculty_dashboard.html',
                                   name=name,
                                   subjects=subjects)

        conn.close()
        return "Invalid Login"

    return render_template('login_faculty.html')


# ---------------- ENTER MARKS + ATTENDANCE ---------------- #

@app.route('/enter_results', methods=['GET', 'POST'])
def enter_results():
    

    if request.method == 'POST':
        usn = request.form['usn']
        subject = request.form['subject_code']
        credits = int(request.form['credits'])
        ia = int(request.form['ia_total'])
        see = int(request.form['see_marks'])

        see_converted = see / 2
        total = ia + see_converted

        grade, gp = calculate_grade(total)

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO results (usn, subject_code, credits, ia_total, see_marks, total, grade, grade_point)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (usn, subject, credits, ia, see, total, grade, gp))

        conn.commit()
        conn.close()

        return redirect('/enter_results')

    return render_template('enter_results.html')
@app.route('/student_report')
def student_report():
    import sqlite3

    usn = request.args.get('usn')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    #  GET MARKS
    cursor.execute('''
        SELECT subject_code, ia1, ia2, ia3, attendance
        FROM marks
        WHERE usn=?
    ''', (usn,))
    rows = cursor.fetchall()

    #  GET STUDENT DETAILS (UPDATED)
    cursor.execute("SELECT name, department, semester FROM student WHERE usn=?", (usn,))
    student = cursor.fetchone()

    name = student[0] if student else "Student"
    department = student[1] if student else "CSE"
    semester = student[2] if student else "6"

    conn.close()

    data = []
    total = 0

    for r in rows:
        best_two = sorted([r[1], r[2], r[3]], reverse=True)[:2]
        avg = sum(best_two) / 2
        total += avg

        data.append({
            "subject": r[0],
            "ia1": r[1],
            "ia2": r[2],
            "ia3": r[3],
            "best": avg,
            "attendance": r[4],
            "warning": r[4] < 80
        })

    sgpa = round(total / len(data) / 10, 2) if data else 0

    return render_template('student_report.html',
                           data=data,
                           sgpa=sgpa,
                           usn=usn,
                           name=name,
                           department=department,
                           semester=semester)
@app.route('/student_results')
def student_results():
    import sqlite3

    usn = request.args.get('usn')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # FETCH RESULTS
    cursor.execute('''
        SELECT subject_code, credits, total, grade, grade_point
        FROM results WHERE usn=?
    ''', (usn,))
    rows = cursor.fetchall()

    # FETCH STUDENT DETAILS (UPDATED)
    cursor.execute("SELECT name, department, semester FROM student WHERE usn=?", (usn,))
    student = cursor.fetchone()

    name = student[0] if student else "Student"
    department = student[1] if student else "CSE"
    semester = student[2] if student else "6"

    conn.close()

    data = []
    total_points = 0
    total_credits = 0

    for r in rows:
        data.append({
            "subject": r[0],
            "credits": r[1],
            "total": r[2],
            "grade": r[3]
        })

        total_points += r[1] * r[4]
        total_credits += r[1]

    sgpa = round(total_points / total_credits, 2) if total_credits else 0

    return render_template('student_results.html',
                           data=data,
                           sgpa=sgpa,
                           usn=usn,
                           name=name,
                           department=department,
                           semester=semester)
@app.route('/enter_marks', methods=['GET', 'POST'])
def enter_marks():
    import sqlite3

    subject = request.args.get('sub')
    name = request.args.get('name')

    if request.method == 'POST':
        usn = request.form['usn']
        ia1 = request.form['ia1']
        ia2 = request.form['ia2']
        ia3 = request.form['ia3']
        attendance = request.form['attendance']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO marks (usn, subject_code, ia1, ia2, ia3, attendance)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (usn, subject, ia1, ia2, ia3, attendance))

        conn.commit()
        conn.close()

        return redirect(f"/enter_marks?sub={subject}&name={name}")

    return render_template('enter_marks.html',
                           subject=subject,
                           name=name)

# ---------------- RUN ---------------- #

if __name__ == '__main__':
    app.run(debug=True)