from save_preset import save_preset, load_preset
def getCurrentSalary():
    baseValue = None
    currentBonus = None
    percentIncrease = None

    # Check if saved values are present
    saved_values = load_preset()
    if 'base_value' in saved_values:
        baseValue = saved_values['base_value']
    else:
        baseValue = int(input("Please enter the base value: ") or 29010)

    if 'current_bonus' in saved_values:
        currentBonus = saved_values['current_bonus']
    else:
        currentBonus = int(input("Please enter the current bonus: ") or 5802)

    if 'percent_increase' in saved_values:
        percentIncrease = saved_values['percent_increase']
    else:
        while True:
            try:
                percentIncrease = int(input("Please enter the percent increase (only value without %): "))
                break
            except ValueError:
                print("Invalid input. Please enter a number.")

    # Save preset values if not loaded
    save_preset(baseValue, currentBonus)

    return baseValue, currentBonus, percentIncrease