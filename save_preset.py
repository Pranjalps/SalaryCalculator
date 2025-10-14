 

import json

def get_user_input(prompt):
    while True:
        try:
            value = int(input(f"Please enter {prompt}: "))
            if 0 <= value <= 10000000:  # Ensure input is within a reasonable range
                return value
            else:
                print("Invalid input. Please enter a number within the specified range.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def save_preset(values):
    try:
        with open('preset.json', 'w') as f:
            json.dump(values, f)
    except Exception as e:
        print(f"Error saving preset values: {e}")

def load_preset():
    try:
        with open('preset.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}