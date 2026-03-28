# MahaParihara - Academic Management System

##  Description
MahaParihara is a role-based academic management system designed to manage student data, marks, attendance, and semester results efficiently.

---

## Features
- Role-based login (Admin, HOD, Faculty, Student)
- Student and faculty registration
- Faculty can enter internal marks and attendance
- Admin can enter semester results
- Automatic SGPA calculation
- HOD can view department results
- Students can view results and download reports (PDF)

---

##  Technologies Used
- Python (Flask)
- SQLite Database
- HTML, CSS
- JavaScript

---

## Modules

###  Admin
- Register students and faculty
- Enter semester results

### Faculty
- Enter IA1, IA2, IA3 marks
- Update attendance

###  HOD
- Assign faculty to subjects
- View internal and semester results

###  Student
- View internal marks and attendance
- View semester results
- SGPA calculation
- Download report

---

##  SGPA Calculation
SGPA = Σ (Credits × Grade Points) / Σ Credits

Grades are assigned based on total marks.

---

##  Project Structure
MahaParihara/
│── app.py
│── database.py
│── templates/
│── static/

---

## Future Enhancements
- CGPA calculation
- Advanced analytics dashboard
- Cloud deployment

---

## Conclusion
This system simplifies academic data management with real-time updates and role-based access.