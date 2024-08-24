import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry


# Main Application Class
class TimesheetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fortnightly Timesheet Submission")

        self.current_view = "staff"
        self.staff_timesheet_data = {}

        self.staff_members = ["Prasanna", "Jeena", "Alex", "Irina", "Kiri"]

        self.create_staff_view()

    # Create the staff view where staff can input their hours, select the period, and add activity descriptions
    def create_staff_view(self):
        self.clear_view()

        tk.Label(self.root, text="Staff Timesheet Submission", font=('Arial', 16)).grid(row=0, column=0, columnspan=5)

        tk.Label(self.root, text="Select Staff Member:", font=('Arial', 12)).grid(row=1, column=0, sticky="e")
        self.staff_name_var = tk.StringVar(value=self.staff_members[0])
        tk.OptionMenu(self.root, self.staff_name_var, *self.staff_members).grid(row=1, column=1, columnspan=4,
                                                                                sticky="w")

        tk.Label(self.root, text="Select Period Start Date:", font=('Arial', 12)).grid(row=2, column=0, sticky="e")
        self.start_date = DateEntry(self.root, date_pattern="yyyy-mm-dd")
        self.start_date.grid(row=2, column=1, columnspan=4, sticky="w")

        tk.Label(self.root, text="Day", font=('Arial', 12)).grid(row=3, column=0)
        tk.Label(self.root, text="Week 1 (No. of hours) Description", font=('Arial', 12)).grid(row=3, column=1,
                                                                                               columnspan=2)
        tk.Label(self.root, text="Week 2 (No. of hours) Description", font=('Arial', 12)).grid(row=3, column=3,
                                                                                               columnspan=2)

        self.entries = {}
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        for i, day in enumerate(days):
            tk.Label(self.root, text=day, font=('Arial', 10)).grid(row=i + 4, column=0, sticky="e")
            entry1 = tk.Entry(self.root)
            entry_desc1 = tk.Entry(self.root, width=20)
            entry2 = tk.Entry(self.root)
            entry_desc2 = tk.Entry(self.root, width=20)
            entry1.grid(row=i + 4, column=1)
            entry_desc1.grid(row=i + 4, column=2)
            entry2.grid(row=i + 4, column=3)
            entry_desc2.grid(row=i + 4, column=4)
            self.entries[day] = (entry1, entry_desc1, entry2, entry_desc2)

        tk.Button(self.root, text="Submit Timesheet", command=self.submit_timesheet).grid(row=9, column=0, columnspan=5,
                                                                                          pady=10)

        tk.Label(self.root, text="Total Hours for 2 Weeks:", font=('Arial', 12)).grid(row=10, column=0, sticky="e")
        self.total_hours_var = tk.StringVar(value="0")
        tk.Label(self.root, textvariable=self.total_hours_var, font=('Arial', 12)).grid(row=10, column=1, columnspan=4,
                                                                                        sticky="w")

    # Clear the current view
    def clear_view(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Submit the timesheet and calculate the total hours
    def submit_timesheet(self):
        self.staff_timesheet_data = {
            "name": self.staff_name_var.get(),
            "start_date": self.start_date.get(),
            "hours": {day: (entry1.get(), entry_desc1.get(), entry2.get(), entry_desc2.get()) for
                      day, (entry1, entry_desc1, entry2, entry_desc2) in self.entries.items()}
        }

        total_hours = 0
        for day, (entry1, desc1, entry2, desc2) in self.entries.items():
            week1_hours = float(entry1.get() or 0)
            week2_hours = float(entry2.get() or 0)

            # Check for public holidays (you might define a function to check this or have a specific list of dates)
            if desc1.get().lower() == "public holiday":
                desc1.delete(0, tk.END)
                desc1.insert(0, "SK77")
            if desc2.get().lower() == "public holiday":
                desc2.delete(0, tk.END)
                desc2.insert(0, "SK77")

            total_hours += week1_hours + week2_hours

        self.total_hours_var.set(str(total_hours))

        messagebox.showinfo("Submission", f"Timesheet submitted successfully for {self.staff_timesheet_data['name']}!")
        self.current_view = "manager"
        self.create_manager_view()

    # Create the manager view for reviewing the timesheet
    def create_manager_view(self):
        self.clear_view()

        tk.Label(self.root, text="Manager Review", font=('Arial', 16)).grid(row=0, column=0, columnspan=5)

        tk.Label(self.root, text=f"Staff Member: {self.staff_timesheet_data['name']}", font=('Arial', 12)).grid(row=1,
                                                                                                                column=0,
                                                                                                                columnspan=5)
        tk.Label(self.root, text=f"Period Start Date: {self.staff_timesheet_data['start_date']}",
                 font=('Arial', 12)).grid(row=2, column=0, columnspan=5)

        tk.Label(self.root, text="Day", font=('Arial', 12)).grid(row=3, column=0)
        tk.Label(self.root, text="Week 1 (No. of hours) Description", font=('Arial', 12)).grid(row=3, column=1,
                                                                                               columnspan=2)
        tk.Label(self.root, text="Week 2 (No. of hours) Description", font=('Arial', 12)).grid(row=3, column=3,
                                                                                               columnspan=2)

        for i, (day, (week1, activity_desc1, week2, activity_desc2)) in enumerate(
                self.staff_timesheet_data['hours'].items()):
            tk.Label(self.root, text=day, font=('Arial', 10)).grid(row=i + 4, column=0, sticky="e")
            tk.Label(self.root, text=week1, font=('Arial', 10)).grid(row=i + 4, column=1)
            tk.Label(self.root, text=activity_desc1, font=('Arial', 10)).grid(row=i + 4, column=2)
            tk.Label(self.root, text=week2, font=('Arial', 10)).grid(row=i + 4, column=3)
            tk.Label(self.root, text=activity_desc2, font=('Arial', 10)).grid(row=i + 4, column=4)

        tk.Label(self.root, text="Total Hours for 2 Weeks:", font=('Arial', 12)).grid(row=9, column=0, sticky="e")
        tk.Label(self.root, text=self.total_hours_var.get(), font=('Arial', 12)).grid(row=9, column=1, columnspan=4,
                                                                                      sticky="w")

        tk.Button(self.root, text="Approve Timesheet", command=self.approve_timesheet).grid(row=10, column=0, pady=10)
        tk.Button(self.root, text="Reject Timesheet", command=self.reject_timesheet).grid(row=10, column=1, pady=10)

    # Approve the timesheet and send it to the finance team
    def approve_timesheet(self):
        messagebox.showinfo("Approval", "Timesheet approved and sent to the finance team!")
        self.create_staff_view()  # Reset to staff view

    # Reject the timesheet and return to staff view for corrections
    def reject_timesheet(self):
        messagebox.showwarning("Rejection", "Timesheet rejected. Please make corrections.")
        self.create_staff_view()


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = TimesheetApp(root)
    root.mainloop()
