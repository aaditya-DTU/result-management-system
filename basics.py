import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

class StudentResultDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Dashboard")
        self.root.geometry("700x500")

        # Labels and Entries for student information
        self.name_label = tk.Label(root, text="Student Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.roll_label = tk.Label(root, text="Roll Number:")
        self.roll_label.grid(row=1, column=0, padx=10, pady=10)
        self.roll_entry = tk.Entry(root)
        self.roll_entry.grid(row=1, column=1, padx=10, pady=10)

        # Subject labels and entries
        self.subjects = ["Math", "Science", "English", "History", "Geography"]
        self.marks_entries = {}

        for i, subject in enumerate(self.subjects):
            label = tk.Label(root, text=f"{subject} Marks:")
            label.grid(row=i+2, column=0, padx=10, pady=5)
            entry = tk.Entry(root)
            entry.grid(row=i+2, column=1, padx=10, pady=5)
            self.marks_entries[subject] = entry

        # Buttons to display the result and save data
        self.result_button = tk.Button(root, text="Show Result", command=self.show_result)
        self.result_button.grid(row=len(self.subjects)+2, column=0, padx=10, pady=10)

        self.save_button = tk.Button(root, text="Save Result", command=self.save_result)
        self.save_button.grid(row=len(self.subjects)+2, column=1, padx=10, pady=10)

        # Canvas for displaying the chart
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=len(self.subjects)+3, padx=10, pady=10)

    def calculate_grade(self, percentage):
        """Function to calculate the grade based on the percentage."""
        if percentage >= 90:
            return "A"
        elif percentage >= 80:
            return "B"
        elif percentage >= 70:
            return "C"
        elif percentage >= 60:
            return "D"
        else:
            return "F"

    def show_result(self):
        try:
            student_name = self.name_entry.get()
            marks = {subject: int(entry.get()) for subject, entry in self.marks_entries.items()}
            total_marks = sum(marks.values())
            percentage = (total_marks / (len(self.subjects) * 100)) * 100
            grade = self.calculate_grade(percentage)

            # Update chart
            self.ax.clear()
            self.ax.bar(marks.keys(), marks.values(), color='green')
            self.ax.set_title(f"{student_name}'s Marks Distribution")
            self.ax.set_xlabel("Subjects")
            self.ax.set_ylabel("Marks")
            self.canvas.draw()

            # Show percentage and grade
            messagebox.showinfo("Result", f"Total Marks: {total_marks}\nPercentage: {percentage:.2f}%\nGrade: {grade}")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid marks for all subjects.")

    def save_result(self):
        try:
            student_name = self.name_entry.get()
            roll_number = self.roll_entry.get()
            marks = {subject: int(entry.get()) for subject, entry in self.marks_entries.items()}
            total_marks = sum(marks.values())
            percentage = (total_marks / (len(self.subjects) * 100)) * 100
            grade = self.calculate_grade(percentage)

            with open('student_results.csv', 'a', newline='') as csvfile:
                fieldnames = ['Name', 'Roll Number'] + self.subjects + ['Total Marks', 'Percentage', 'Grade']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

# Write the header only once (if the file is empty)
                if csvfile.tell() == 0:
                    writer.writeheader()

                row_data = {
                    'Name': student_name,
                    'Roll Number': roll_number,
                    **marks,
                    'Total Marks': total_marks,
                    'Percentage': percentage,
                    'Grade': grade
                }

                writer.writerow(row_data)

            messagebox.showinfo("Saved", "Student result has been saved successfully!")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid marks for all subjects.")

# Running the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentResultDashboard(root)
    root.mainloop()