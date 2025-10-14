import json

# Initialize an empty dictionary to store preset values
preset_values = []

def save_preset(base_value, current_bonus):
    """Save preset values to a file."""
    preset_values = {
        'base_value': base_value,
        'current_bonus': current_bonus,}
    filename = 'preset.json'
    try:
        with open(filename, 'w') as f:
            json.dump(preset_values, f)
    except Exception as e:
        print(f"Error saving preset values: {e}")

def load_preset():
    """Load preset values from a file."""
    preset_values
    filename = 'preset.json'
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
