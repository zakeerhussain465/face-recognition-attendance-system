import tkinter as tk
import subprocess

root = tk.Tk()
root.title("Face Recognition Attendance")
root.geometry("400x300")

label = tk.Label(root, text="Face Recognition Attendance System", font=("Arial", 14))
label.pack(pady=20)

def start_attendance():
    subprocess.Popen(["python", "main.py"])

def register_student():
    subprocess.Popen(["python", "register_student.py"])

btn1 = tk.Button(root, text="Start Attendance", command=start_attendance, width=20)
btn1.pack(pady=10)

btn2 = tk.Button(root, text="Register New Student", command=register_student, width=20)
btn2.pack(pady=10)

root.mainloop()
