import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime

class Grade11ICTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grade 11 ICT Acacia Management App")
        self.root.geometry("800x600")

        # Initialize data storage
        self.students = []
        self.funds = []
        self.plans = []
        self.attendance = {}
        self.history = []

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        # Title Frame
        title_frame = tk.Frame(self.root, bg="#FFCCF9", padx=10, pady=10)
        title_frame.pack(fill="x")
        title = tk.Label(title_frame, text="Grade 11 ICT Acacia Management App", font=("Comic Sans MS", 18, "bold"), bg="#FFCCF9", fg="#F72585")
        title.pack()

        # Main Frame with Scrollable Content
        self.main_frame = tk.Frame(self.root, bg="#FFF0F5")
        self.main_frame.pack(fill="both", expand=True)

        # Create a canvas and scrollbar
        self.canvas = tk.Canvas(self.main_frame, bg="#FFF0F5")
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFF0F5")

        # Configure scrollbar
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Setup individual sections
        self.setup_student_section(self.scrollable_frame)
        self.setup_funds_section(self.scrollable_frame)
        self.setup_action_plans_section(self.scrollable_frame)
        self.setup_attendance_tracker(self.scrollable_frame)
        self.setup_history_section(self.scrollable_frame)

    def setup_student_section(self, main_frame):
        student_frame = tk.Frame(main_frame, bg="#A0E7E5", padx=5, pady=5, bd=2, relief="groove")
        student_frame.pack(fill="x", padx=10, pady=5)
        student_label = tk.Label(student_frame, text="Students", font=("Arial", 12, "bold"), bg="#A0E7E5")
        student_label.pack()
        self.student_listbox = tk.Listbox(student_frame, width=30, height=5, bg="#FFFAE3", font=("Arial", 10))
        self.student_listbox.pack(pady=5)
        add_student_btn = tk.Button(student_frame, text="Add Student", command=self.add_student, bg="#FFB5E8")
        add_student_btn.pack(fill="x", pady=2)
        edit_student_btn = tk.Button(student_frame, text="Edit Student", command=self.edit_student, bg="#FFB5E8")
        edit_student_btn.pack(fill="x", pady=2)
        remove_student_btn = tk.Button(student_frame, text="Remove Student", command=self.remove_student, bg="#FFB5E8")
        remove_student_btn.pack(fill="x", pady=2)

    def setup_funds_section(self, main_frame):
        funds_frame = tk.Frame(main_frame, bg="#BDE0FE", padx=5, pady=5, bd=2, relief="groove")
        funds_frame.pack(fill="x", padx=10, pady=5)
        funds_label = tk.Label(funds_frame, text="Funds", font=("Arial", 12, "bold"), bg="#BDE0FE")
        funds_label.pack()
        self.funds_listbox = tk.Listbox(funds_frame, width=30, height=5, bg="#FFFAE3", font=("Arial", 10))
        self.funds_listbox.pack(pady=5)
        add_fund_btn = tk.Button(funds_frame, text="Add Fund", command=self.add_fund, bg="#A0C4FF")
        add_fund_btn.pack(fill="x", pady=2)
        remove_fund_btn = tk.Button(funds_frame, text="Remove Fund", command=self.remove_fund, bg="#A0C4FF")
        remove_fund_btn.pack(fill="x", pady=2)
        self.total_funds_label = tk.Label(funds_frame, text="Total Funds: PHP 0.00", font=("Arial", 10, "bold"), bg="#BDE0FE")
        self.total_funds_label.pack(pady=5)

    def setup_action_plans_section(self, main_frame):
        plans_frame = tk.Frame(main_frame, bg="#FFCCF9", padx=5, pady=5, bd=2, relief="groove")
        plans_frame.pack(fill="x", padx=10, pady=5)
        plans_label = tk.Label(plans_frame, text="Action Plans", font=("Arial", 12, "bold"), bg="#FFCCF9")
        plans_label.pack()
        self.plan_listbox = tk.Listbox(plans_frame, width=50, height=5, bg="#FFFAE3", font=("Arial", 10))
        self.plan_listbox.pack(pady=5)
        add_plan_btn = tk.Button(plans_frame, text="Add Plan", command=self.add_plan, bg="#CDB4DB")
        add_plan_btn.pack(fill="x", pady=2)
        remove_plan_btn = tk.Button(plans_frame, text="Remove Plan", command=self.remove_plan, bg="#CDB4DB")
        remove_plan_btn.pack(fill="x", pady=2)

    def setup_attendance_tracker(self, main_frame):
        attendance_frame = tk.Frame(main_frame, bg="#FFD6A5", padx=5, pady=5, bd=2, relief="groove")
        attendance_frame.pack(fill="x", padx=10, pady=5)
        attendance_label = tk.Label(attendance_frame, text="Attendance Tracker", font=("Arial", 12, "bold"), bg="#FFD6A5")
        attendance_label.pack()

        self.attendance_frame = tk.Frame(attendance_frame, bg="#FFD6A5")
        self.attendance_frame.pack(fill="x")

        self.attendance_listbox = tk.Listbox(self.attendance_frame, height=10, bg="#FFFAE3", font=("Arial", 10))
        self.attendance_listbox.pack(side="left", fill="both", expand=True)
        self.attendance_scrollbar = tk.Scrollbar(self.attendance_frame, command=self.attendance_listbox.yview)
        self.attendance_listbox.config(yscrollcommand=self.attendance_scrollbar.set)
        self.attendance_scrollbar.pack(side="right", fill="y")

        self.days_buttons = []
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
            btn = tk.Button(attendance_frame, text=day, width=10, bg="#FFADAD", command=lambda d=day: self.toggle_attendance(d))
            btn.pack(side="left", padx=5)
            self.days_buttons.append((day, btn))

    def setup_history_section(self, main_frame):
        history_frame = tk.Frame(main_frame, bg="#CAF0F8", padx=10, pady=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=10)
        history_label = tk.Label(history_frame, text="History Log", font=("Arial", 12, "bold"), bg="#CAF0F8")
        history_label.pack()
        self.history_listbox = tk.Listbox(history_frame, width=75, height=10, bg="#FFFAE3", font=("Arial", 10))
        self.history_listbox.pack()

    def get_timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def log_history(self, action):
        timestamp = self.get_timestamp()
        self.history.append(f"{timestamp} - {action}")
        self.history_listbox.insert(tk.END, f"{timestamp} - {action}")

    def add_student(self):
        student_name = simpledialog.askstring("Add Student", "Enter student's name:")
        if student_name:
            self.students.append(student_name)
            self.student_listbox.insert(tk.END, student_name)
            self.attendance[student_name] = {day: "Present" for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]}
            self.update_attendance_list()
            self.log_history(f"Added student: {student_name}")

    def edit_student(self):
        selected_student = self.student_listbox.curselection()
        if not selected_student:
            messagebox.showwarning("Select Student", "Please select a student to edit.")
            return
        student_index = selected_student[0]
        student_name = self.students[student_index]
        new_name = simpledialog.askstring("Edit Student", "Edit student's name:", initialvalue=student_name)
        if new_name:
            self.students[student_index] = new_name
            self.student_listbox.delete(student_index)
            self.student_listbox.insert(student_index, new_name)
            self.update_attendance_list()
            self.log_history(f"Edited student: {student_name} to {new_name}")

    def remove_student(self):
        selected_student = self.student_listbox.curselection()
        if not selected_student:
            messagebox.showwarning("Select Student", "Please select a student to remove.")
            return
        student_index = selected_student[0]
        student_name = self.students[student_index]
        del self.attendance[student_name]  # Remove attendance data
        self.students.pop(student_index)
        self.student_listbox.delete(student_index)
        self.update_attendance_list()
        self.log_history(f"Removed student: {student_name}")

    def toggle_attendance(self, day):
        selected_student = self.student_listbox.curselection()
        if not selected_student:
            messagebox.showwarning("Select Student", "Please select a student to toggle attendance.")
            return
        student_index = selected_student[0]
        student_name = self.students[student_index]
        current_status = self.attendance[student_name][day]
        new_status = "Absent" if current_status == "Present" else "Present"
        self.attendance[student_name][day] = new_status
        self.update_attendance_list()
        self.log_history(f"Toggled {student_name}'s attendance on {day} to {new_status}")

    def update_attendance_list(self):
        self.attendance_listbox.delete(0, tk.END)
        for student in self.students:
            attendance_status = ', '.join([f"{day}: {self.attendance[student][day]}" for day in self.attendance[student]])
            self.attendance_listbox.insert(tk.END, f"{student} - {attendance_status}")

    def add_fund(self):
        description = simpledialog.askstring("Add Fund", "Enter fund description:")
        amount = simpledialog.askfloat("Add Fund", "Enter fund amount:")
        if description and amount:
            self.funds.append((description, amount))
            self.funds_listbox.insert(tk.END, f"{description}: PHP {amount:.2f}")
            self.update_total_funds()
            self.log_history(f"Added fund - {description}: PHP {amount:.2f}")

    def remove_fund(self):
        selected_fund = self.funds_listbox.curselection()
        if not selected_fund:
            messagebox.showwarning("Select Fund", "Please select a fund to remove.")
            return
        fund_index = selected_fund[0]
        fund_description = self.funds[fund_index][0]
        self.funds.pop(fund_index)
        self.funds_listbox.delete(fund_index)
        self.update_total_funds()
        self.log_history(f"Removed fund - {fund_description}")

    def update_total_funds(self):
        total = sum(amount for _, amount in self.funds)
        self.total_funds_label.config(text=f"Total Funds: PHP {total:.2f}")

    def add_plan(self):
        plan = simpledialog.askstring("Add Action Plan", "Enter action plan:")
        if plan:
            self.plans.append(plan)
            self.plan_listbox.insert(tk.END, plan)
            self.log_history(f"Added action plan: {plan}")

    def remove_plan(self):
        selected_plan = self.plan_listbox.curselection()
        if not selected_plan:
            messagebox.showwarning("Select Plan", "Please select an action plan to remove.")
            return
        plan_index = selected_plan[0]
        plan_description = self.plans[plan_index]
        self.plans.pop(plan_index)
        self.plan_listbox.delete(plan_index)
        self.log_history(f"Removed action plan: {plan_description}")

# Create and run the app
root = tk.Tk()
app = Grade11ICTApp(root)
root.mainloop()
