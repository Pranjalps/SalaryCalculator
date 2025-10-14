import secrets
import json
import tkinter as tk
from tkinter import messagebox, filedialog, Label
import sqlite3

class SalaryCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Salary Calculator")
        self.presets = {}
        self.calculations = []
        self.db_name = 'salary_calculator.db'
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        """
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
        tk.Button(root, text="Load Preset", command=self.load_preset).grid(row=5, column=0, columnspan=2)
        tk.Button(root, text="Update Preset", command=self.update_preset).grid(row=6, column=0, columnspan=2)

        # Create labels to display output
        self.output_label = Label(root, text="", wraplength=400)
        self.output_label.grid(row=7, column=0, columnspan=2)"""
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS calculations
            (id INTEGER PRIMARY KEY, base_value REAL, current_bonus REAL, percent_increase REAL, new_basic REAL, new_allowance REAL, new_pf REAL, new_gratuity REAL, new_salary REAL, ctc REAL, in_hand REAL)
        ''')
        self.conn.commit()
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

        if len(self.calculations) > 10:
            self.calculations.pop(0)

        new_basic = int(self.base_value_entry.get()) + (int(self.base_value_entry.get()) * (float(self.percent_increase_entry.get()) / 100))
        new_allowance = int(new_basic) * 0.63 + int(self.current_bonus_entry.get())
        new_pf = int(new_basic) * 0.12
        new_gratuity = int(new_basic) * 0.05
        new_salary = int(new_basic) + int(new_allowance) + int(new_pf) + int(new_gratuity)
        ctc = int(new_salary) * 12
        in_hand = int(new_basic) + int(new_allowance) - int(new_pf)
        self.calculations.append({
            'base_value': int(self.base_value_entry.get()),
            'current_bonus': int(self.current_bonus_entry.get()),
            'percent_increase': float(self.percent_increase_entry.get()),
            'new_basic': int(new_basic),
            'new_allowance': int(new_allowance), 
            'new_pf': int(new_pf),
            'new_gratuity': int(new_gratuity),
            'new_salary': int(new_salary),
            'ctc': int(ctc),
            'in_hand': int(in_hand)
        })
        
        
        self.update_labels()
        self.save_to_database()

    def store_preset(self):
        name = filedialog.asksaveasfilename(defaultextension=".json")
        if not name:
            return

        base_value = int(self.base_value_entry.get())
        current_bonus = int(self.current_bonus_entry.get())
        percent_increase = float(self.percent_increase_entry.get())

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

        base_value = int(self.base_value_entry.get())
        current_bonus = int(self.current_bonus_entry.get())
        percent_increase = float(self.percent_increase_entry.get())

        self.presets[name] = {
            'base_value': base_value,
            'current_bonus': current_bonus,
            'percent_increase': percent_increase
        }

        with open(name, 'w') as f:
            json.dump(self.presets, f)

    def update_labels(self):
        for i, calculation in enumerate(self.calculations):
            #tk.Label(self.root, text=f"Calculation {i+1}:").grid(row=i+8, column=0)
            tk.Label(self.root, text="Base Value: " + str(calculation['base_value'])).grid(row=i+9, column=0)
            tk.Label(self.root, text="Current Bonus: " + str(calculation['current_bonus'])).grid(row=i+10, column=0)
            tk.Label(self.root, text="Percent Increase: " + str(calculation['percent_increase'])).grid(row=i+11, column=0)
            tk.Label(self.root, text="New Basic: " + str(calculation.get('new_basic', 0))).grid(row=i+9, column=1)
            tk.Label(self.root, text="New Allowance: " + str(calculation.get('new_allowance', 0))).grid(row=i+10, column=1)
            tk.Label(self.root, text="New PF: " + str(calculation.get('new_pf', 0))).grid(row=i+11, column=1)
            tk.Label(self.root, text="New Gratuity: " + str(calculation.get ('new_gratuity', 0))).grid(row=i+9, column=2)
            tk.Label(self.root, text="New Salary: " + str(calculation.get('new_salary', 0))).grid(row=i+10, column=2)
            tk.Label(self.root, text="CTC: " + str(calculation.get('ctc', 0))).grid(row=i+11, column=2)
            tk.Label(self.root, text="In-hand salary: " + str(calculation.get('in_hand', 0))).grid(row=i+9, column=3)   
    def save_to_database(self):
        for calculation in self.calculations:
            self.cursor.execute('''
                INSERT INTO calculations (base_value, current_bonus, percent_increase, new_basic, new_allowance, new_pf, new_gratuity, new_salary, ctc, in_hand)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (calculation['base_value'], calculation['current_bonus'], calculation['percent_increase'], calculation['new_basic'], calculation['new_allowance'], 
                  calculation['new_pf'], calculation['new_gratuity'], calculation['new_salary'], calculation['ctc'], calculation['in_hand']))
        self.conn.commit()
    def display_calculations(self):
        for i in range(8, len(self.calculations)+9):
            #tk.Label(self.root, text=f"Calculation {i-7}:").grid(row=i, column=0)
            if i >= 9:
                base_value = self.calculations[i-8].get('base_value', 0)
                current_bonus = self.calculations[i-8].get('current_bonus', 0)
                percent_increase = self.calculations[i-8].get('percent_increase', 0)

                tk.Label(self.root, text="Base Value: " + str(base_value)).grid(row=i, column=1)
                tk.Label(self.root, text="Current Bonus: " + str(current_bonus)).grid(row=i, column=2)
                tk.Label(self.root, text="Percent Increase: " + str(percent_increase)).grid(row=i, column=3)

            if i >= 9:
                new_basic = self.calculations[i-8].get('new_basic', 0)
                new_allowance = self.calculations[i-8].get('new_allowance', 0)
                new_pf = self.calculations[i-8].get('new_pf', 0)
                new_gratuity = self.calculations[i-8].get('new_gratuity', 0)
                new_salary = self.calculations[i-8].get('new_salary', 0)
                ctc = self.calculations[i-8].get('ctc', 0)
                in_hand = self.calculations[i-8].get('in_hand', 0)

                tk.Label(self.root, text="New Basic: " + str(new_basic)).grid(row=i, column=4)
                tk.Label(self.root, text="New Allowance: " + str(new_allowance)).grid(row=i, column=5)
                tk.Label(self.root, text="New PF: " + str(new_pf)).grid(row=i, column=6)
                tk.Label(self.root, text="New Gratuity: " + str(new_gratuity)).grid(row=i, column=7)
                tk.Label(self.root, text="New Salary: " + str(new_salary)).grid(row=i, column=8)
                tk.Label(self.root, text="CTC: " + str(ctc)).grid(row=i, column=9)
                tk.Label(self.root, text="In-hand salary: " + str(in_hand)).grid(row=i, column=10)
        
    def search_calculations(self):
        id = self.search_entry.get()
        if not id:
            return

        try:
            id = int(id)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter an integer.")
            return

        self.cursor.execute('SELECT * FROM calculations WHERE id=?', (id,))
        result = self.cursor.fetchone()

        if not result:
            messagebox.showinfo("Result", "No calculation found with ID " + str(id))
            return

        self.search_window = tk.Toplevel(self.root)
        self.search_label = Label(self.search_window, text="Search Results:")
        self.search_label.grid(row=0, column=0)

        tk.Label(self.search_window, text="Base Value: ").grid(row=1, column=0)
        tk.Label(self.search_window, text=str(result[1])).grid(row=1, column=1)

        tk.Label(self.search_window, text="Current Bonus: ").grid(row=2, column=0)
        tk.Label(self.search_window, text=str(result[2])).grid(row=2, column=1)

        tk.Label(self.search_window, text="Percent Increase: ").grid(row=3, column=0)
        tk.Label(self.search_window, text=str(result[3])).grid(row=3, column=1)

        tk.Label(self.search_window, text="New Basic: ").grid(row=4, column=0)
        tk.Label(self.search_window, text=str(result[4])).grid(row=4, column=1) 

        tk.Label(self.search_window, text="New Allowance: ").grid(row=5, column=0)
        tk.Label(self.search_window, text=str(result[5])).grid(row=5, column=1)

        tk.Label(self.search_window, text="New PF: ").grid(row=6, column=0)
        tk.Label(self.search_window, text=str(result[6])).grid(row=6, column=1)

        tk.Label(self.search_window, text="New Gratuity: ").grid(row=7, column=0)
        tk.Label(self.search_window, text=str(result[7])).grid(row=7, column=1)

        tk.Label(self.search_window, text="New Salary: ").grid(row=8, column=0)
        tk.Label(self.search_window, text=str(result[8])).grid(row=8, column=1)

        tk.Label(self.search_window, text="CTC: ").grid(row=9, column=0)
        tk.Label(self.search_window, text=str(result[9])).grid(row=9, column=1)

        tk.Label(self.search_window, text="In-hand salary: ").grid(row=10, column=0)
        tk.Label(self.search_window, text=str(result[10])).grid(row=10, column=1)   

    def delete_calculation(self):
        id = self.delete_entry.get()
        if not id:
            return

        try:
            id = int(id)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter an integer.")
            return

        self.cursor.execute('DELETE FROM calculations WHERE id=?', (id,))
        self.conn.commit()

        messagebox.showinfo("Result", "Calculation with ID " + str(id) + " deleted")

    def update_window(self):
        self.update_window = tk.Toplevel(self.root)
        self.update_label = Label(self.update_window, text="Update")
        self.update_label.grid(row=0, column=0)

        tk.Label(self.update_window, text="Base Value: ").grid(row=1, column=0)
        tk.Entry(self.update_window).grid(row=1, column=1)

        tk.Label(self.update_window, text="Current Bonus: ").grid(row=2, column=0)
        tk.Entry(self.update_window).grid(row=2, column=1)

        tk.Label(self.update_window, text="Percent Increase: ").grid(row=3, column=0)
        tk.Entry(self.update_window).grid(row=3, column=1)
    def main(self):
        self.create_table()
        self.base_value_label = Label(self.root, text="Base Value:")
        self.base_value_label.grid(row=0, column=0)
        self.base_value_entry = tk.Entry(self.root)
        self.base_value_entry.grid(row=0, column=1)

        self.current_bonus_label = Label(self.root, text="Current Bonus:")
        self.current_bonus_label.grid(row=1, column=0)
        self.current_bonus_entry = tk.Entry(self.root)
        self.current_bonus_entry.grid(row=1, column=1)

        self.percent_increase_label = Label(self.root, text="Percent Increase:")
        self.percent_increase_label.grid(row=2, column=0)
        self.percent_increase_entry = tk.Entry(self.root)
        self.percent_increase_entry.grid(row=2, column=1)

        self.calculate_button = tk.Button(self.root, text="Calculate", command=self.calculate_salary)
        self.calculate_button.grid(row=3, column=0, columnspan=1)

        self.store_button = tk.Button(self.root, text="Store Preset", command=self.store_preset)
        self.store_button.grid(row=3, column=1, columnspan=1)

        self.load_button = tk.Button(self.root, text="Load Preset", command=self.load_preset)
        self.load_button.grid(row=3, column=2, columnspan=1)

        self.update_button = tk.Button(self.root, text="Update Preset", command=self.update_preset)
        self.update_button.grid(row=4, column=0, columnspan=1)

        self.display_button = tk.Button(self.root, text="Display Calculations", command=self.display_calculations)
        self.display_button.grid(row=4, column=1, columnspan=1)

        self.search_label = Label(self.root, text="Search Calculation:")
        self.search_label.grid(row=5, column=0)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=5, column=1)

        self.search_button = tk.Button(self.root, text="Search", command=self.search_calculations)
        self.search_button.grid(row=5, column=3, columnspan=1)

        self.delete_label = Label(self.root, text="Delete Calculation:")
        self.delete_label.grid(row=7, column=0)
        self.delete_entry = tk.Entry(self.root)
        self.delete_entry.grid(row=7, column=1)

        self.delete_button = tk.Button(self.root, text="Delete", command=self.delete_calculation)
        self.delete_button.grid(row=7, column=3, columnspan=1)


    def run(self):
        self.main()
        self.root.mainloop()
if __name__ == "__main__":
    app = SalaryCalculator(tk.Tk())
    app.run()