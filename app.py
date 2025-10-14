import secrets
import json
import tkinter as tk
from tkinter import messagebox, filedialog

class SalaryCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Salary Calculator")
        self.presets = {}

        # Create entry fields for user input
        tk.Label(root, text="Base Value").grid(row=0)
        self.base_value_entry = tk.Entry(root)
        self.base_value_entry.grid(row=0, column=1)

        tk.Label(root, text="Current Bonus").grid(row=1)
        self.current_bonus_entry = tk.Entry(root)
        self.current_bonus_entry.grid(row=1, column=1)

        tk.Label(root, text="Percent Increase").grid(row=2)
        self.percent_increase_entry = tk.Entry(root)
        self.percent_increase_entry.grid(row=2, column=1)

        # Create buttons for calculating salary and storing presets
        tk.Button(root, text="Calculate Salary", command=self.calculate_salary).grid(row=3, column=0, columnspan=2)
        tk.Button(root, text="Store Preset", command=self.store_preset).grid(row=4, column=0, columnspan=2)

        # Create labels to display output
        self.output_label = tk.Label(root, text="", wraplength=400)
        self.output_label.grid(row=5, column=0, columnspan=2)

    def get_user_input(self):
        base_value = self.base_value_entry.get()
        current_bonus = self.current_bonus_entry.get()
        percent_increase = self.percent_increase_entry.get()

        try:
            base_value = int(base_value)
            current_bonus = int(current_bonus)
            percent_increase = float(percent_increase)  # Allow for decimal values
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values.")
            return None, None, None

        if not (0 <= base_value <= 10000000):  # Ensure input is within a reasonable range
            messagebox.showerror("Error", "Base value must be between 0 and 1,000,000")
            return None, None, None

        return base_value, current_bonus, percent_increase

    def calculate_salary(self):
        base_value, current_bonus, percent_increase = self.get_user_input()

        if not all([base_value, current_bonus, percent_increase]):
            return

        new_basic = base_value + (base_value * (percent_increase / 100))
        new_allowance = int(new_basic) * 0.63 + int(current_bonus)
        new_pf = int(new_basic) * 0.12
        new_gratuity = int(new_basic) * 0.05
        new_salary = int(new_basic) + int(new_allowance) + int(new_pf) + int(new_gratuity)
        ctc = int(new_salary) * 12
        in_hand = int(new_basic) + int(new_allowance) - int(new_pf)

        self.output_label['text'] = f"The new salary is: {new_salary}\nThe new basic is: {new_basic}\nThe new allowance is: {new_allowance}\nThe new PF is: {new_pf}\nThe new gratuity is: {new_gratuity}\nThe new CTC is: {ctc}\nThe new in-hand salary is: {in_hand}"

    def store_preset(self):
        name = filedialog.asksaveasfilename(defaultextension=".json")
        if not name:
            return

        base_value = self.base_value_entry.get()
        current_bonus = self.current_bonus_entry.get()
        percent_increase = self.percent_increase_entry.get()

        try:
            base_value = int(base_value)
            current_bonus = int(current_bonus)
            percent_increase = float(percent_increase)  # Allow for decimal values
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values.")
            return

        if not (0 <= base_value <= 10000000):  # Ensure input is within a reasonable range
            messagebox.showerror("Error", "Base value must be between 0 and 1,000,000")
            return

        self.presets[name] = {
            'base_value': base_value,
            'current_bonus': current_bonus,
            'percent_increase': percent_increase
        }

        with open(name, 'w') as f:
            json.dump(self.presets, f)

    def load_preset(self):
        name = filedialog.askopenfilename(defaultextension=".json")
        if not name:
            return

        try:
            with open(name, 'r') as f:
                self.presets = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "No preset file found")

    def update_preset(self):
        name = filedialog.asksaveasfilename(defaultextension=".json")
        if not name:
            return

        base_value = self.base_value_entry.get()
        current_bonus = self.current_bonus_entry.get()
        percent_increase = self.percent_increase_entry.get()

        try:
            base_value = int(base_value)
            current_bonus = int(current_bonus)
            percent_increase = float(percent_increase)  # Allow for decimal values
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values.")
            return

        if not (0 <= base_value <= 10000000):  # Ensure input is within a reasonable range
            messagebox.showerror("Error", "Base value must be between 0 and 1,000,000")
            return

        self.presets[name] = {
            'base_value': base_value,
            'current_bonus': current_bonus,
            'percent_increase': percent_increase
        }

        with open(name, 'w') as f:
            json.dump(self.presets, f)

if __name__ == "__main__":
    root = tk.Tk()
    app = SalaryCalculator(root)
    root.mainloop()