import sqlite3
from prettytable import PrettyTable

# Connect to SQLite database
conn = sqlite3.connect('college_attendance.db')
c = conn.cursor()

# Create student table
def create_student_table():
    """
    Create a table to store student information.
    Columns: ID (primary key), name, roll number, email, department.
    """
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                    ID INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    roll_no TEXT NOT NULL,
                    email TEXT,
                    department TEXT
                )''')
create_student_table()

# Function to add a new student
def add_student(name, roll_no, email, department):
    """
    Add a new student to the database.
    """
    c.execute("INSERT INTO students (name, roll_no, email, department) VALUES (?, ?, ?, ?)", (name, roll_no, email, department))
    conn.commit()
    print("Student added successfully!")

    # Automatically create attendance table for the new student if not already created
    student_id = c.lastrowid
    c.execute('''CREATE TABLE IF NOT EXISTS attendance_{id} (
                    date DATE PRIMARY KEY,
                    subject1 TEXT,
                    subject2 TEXT,
                    subject3 TEXT,
                    subject4 TEXT,
                    subject5 TEXT
                )'''.format(id=student_id))
    conn.commit()

# Function to mark attendance for a subject
def mark_attendance(student_id, date, subject, status):
    """
    Mark attendance for a subject for a given student on a specific date.
    """
    # Check if attendance record for the given date exists
    c.execute("SELECT * FROM attendance_{id} WHERE date=?".format(id=student_id), (date,))
    existing_record = c.fetchone()

    if existing_record:
        # Update existing attendance record
        c.execute(f"UPDATE attendance_{student_id} SET {subject}=? WHERE date=?", (status, date))
        print("Attendance updated successfully!")
    else:
        # Insert new attendance record
        c.execute(f"INSERT INTO attendance_{student_id} (date, {subject}) VALUES (?, ?)", (date, status))
        print("Attendance marked successfully!")

    conn.commit()

def generate_attendance_report(student_id):
    """
    Generate an attendance report for a given student.
    Report includes:
    - Student's name, roll number, and department
    - Attendance percentage for each subject
    - Overall attendance percentage
    - Attendance table for the student
    """
    # Retrieve student information
    c.execute("SELECT name, roll_no, department FROM students WHERE ID = ?", (student_id,))
    student_info = c.fetchone()

    # Check if student information is fetched successfully
    if student_info:
        student_name, roll_no, department = student_info

        # Create a PrettyTable for the report
        report_table = PrettyTable()
        report_table.field_names = ["Subject", "Attendance Percentage"]

        # Fetch attendance records for the student
        c.execute(f"SELECT * FROM attendance_{student_id}")
        attendance_records = c.fetchall()

        # Initialize variables to calculate overall attendance
        total_classes = len(attendance_records)
        total_attended = 0

        # Count attendance for each subject
        subject_counts = {"Subject 1": 0, "Subject 2": 0, "Subject 3": 0, "Subject 4": 0, "Subject 5": 0}
        subject_totals = {"Subject 1": 0, "Subject 2": 0, "Subject 3": 0, "Subject 4": 0, "Subject 5": 0}
        for record in attendance_records:
            for i in range(1, len(record)):
                subject = f"Subject {i}"
                if record[i] is not None:
                    subject_totals[subject] += 1
                    if record[i] == 'Present':
                        subject_counts[subject] += 1
                        total_attended += 1

        # Calculate and add attendance percentages to the report table
        for subject, count in subject_counts.items():
            if subject_totals[subject] > 0:
                percentage = (count / subject_totals[subject]) * 100
            else:
                percentage = 0.0
            report_table.add_row([subject, "{:.2f}%".format(percentage)])

        # Calculate overall attendance percentage
        if total_classes > 0:
            overall_percentage = (total_attended / (total_classes * len(subject_counts))) * 100
        else:
            overall_percentage = 0.0
        report_table.add_row(["Overall", "{:.2f}%".format(overall_percentage)])

        # Print the report
        print("Attendance Report for Student ID {}: {} ({})".format(student_id, student_name, roll_no))
        print("Department: {}".format(department))
        print(report_table)

        # Print the attendance table
        attendance_table = PrettyTable()
        attendance_table.field_names = ["Date", "Subject 1", "Subject 2", "Subject 3", "Subject 4", "Subject 5"]
        for record in attendance_records:
            attendance_table.add_row(record)

        print("\nAttendance Table:")
        print(attendance_table)
    else:
        print("No student found with ID:", student_id)


# Function to take attendance for a student
def take_attendance(student_id, date):
    """
    Take attendance for a student by inputting the attendance status (present or absent) for each subject.
    """
    print("Enter attendance for student ID {}: (Enter 'P' for Present, 'A' for Absent)".format(student_id))
    for subject_num in range(1, 6):
        subject = f"subject{subject_num}"
        status = input(f"Attendance for {subject}: ").strip().capitalize()  # Ensuring consistent input format
        while status not in ['P', 'A']:
            print("Invalid input. Please enter 'P' for Present or 'A' for Absent.")
            status = input(f"Attendance for {subject}: ").strip().capitalize()
        mark_attendance(student_id, date, subject, 'Present' if status == 'P' else 'Absent')

# Function to input student data
def input_student_data():
    """
    Take input from the user for student information and insert it into the database.
    """
    name = input("Enter student's name: ")
    roll_no = input("Enter student's roll number: ")
    email = input("Enter student's email address: ")
    department = input("Enter student's department: ")
    add_student(name, roll_no, email, department)

# Function to print student table
def print_student_table():
    """
    Fetch all student records from the database and print them in tabular format.
    """
    c.execute("SELECT * FROM students")
    rows = c.fetchall()
    if not rows:
        print("No students found.")
    else:
        print("Student Table:")
        for row in rows:
            print(row)

def delete_student_data(student_id):
    """
    Delete the data of a specific student from the database.
    """
    # Delete student record from the students table
    c.execute("DELETE FROM students WHERE ID=?", (student_id,))
    conn.commit()
    
    # Check if the attendance table for the student exists and delete it
    try:
        c.execute(f"DROP TABLE attendance_{student_id}")
        conn.commit()
        print(f"Attendance data for student ID {student_id} deleted successfully.")
    except sqlite3.OperationalError:
        print(f"No attendance data found for student ID {student_id}.")

def main():
    """
    Main function to demonstrate sample usage of the attendance management system.
    """
    while True:
        print("\n1. Add a new student")
        print("2. Take attendance for a student")
        print("3. Generate attendance report for a student")
        print("4. Print all students")
        print("5. Delete student data")
        print("6. Exit")

        option = input("\nSelect an option: ")

        if option == '1':
            input_student_data()
        elif option == '2':
            student_id = int(input("Enter student ID: "))
            date = input("Enter date (DD-MM-YYYY): ")
            take_attendance(student_id, date)
        elif option == '3':
            student_id = int(input("Enter student ID: "))
            generate_attendance_report(student_id)
        elif option == '4':
            print_student_table()
        elif option == '5':
            student_id = int(input("Enter student ID to delete: "))
            delete_student_data(student_id)
        elif option == '6':
            break
        else:
            print("Invalid option. Please try again.")

# Execute main function
if __name__ == "__main__":
    main()

# Close connection
conn.close()
