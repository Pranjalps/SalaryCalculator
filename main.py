from CalculateSalary import calculate_salary
from save_preset import get_user_input, save_preset, load_preset


def main():
    # Load preset values if available
    presets = load_preset()
    if presets:
        base_value = presets.get('base_value', 0)
        current_bonus = presets.get('current_bonus', 0)
        percent_increase = presets.get('percent_increase', 0)
        print(f"Loaded preset values: Base Value={base_value}, Current Bonus={current_bonus}, Percent Increase={percent_increase}")
    else:
        print("No preset values found. Please enter new values.")
        # Get user inputs
    if base_value == 0 :
        base_value = get_user_input("Please enter the base value: ")
    if current_bonus == 0 :
        current_bonus = get_user_input("Please enter the current bonus: ")
    if percent_increase == 0 :
        percent_increase = get_user_input("Please enter the percent increase (only value without %): ")
    else:
        choice = input("Using preset value for percentage. Do you want to change percentage increase? (yes/no)" or "no")
        if(choice.lower() == "yes"):
            percent_increase = get_user_input("Please enter the percent increase (only value without %): ")
            if percent_increase < 0:
                print("Invalid input. Please enter a non-negative value.")
                return
    # Validate inputs
    if base_value < 0 or current_bonus < 0 or percent_increase < 0:
        print("Invalid input. Please enter non-negative values.")
        return
    # Save preset values if not loaded
    save_preset({
        'base_value': base_value,
        'current_bonus': current_bonus,
        'percent_increase': percent_increase,
    })

    new_salary, new_basic, new_allowance, new_pf, new_gratuity, new_salary, ctc, in_hand = calculate_salary(base_value, current_bonus, percent_increase)

    print("The new salary is: ", new_salary)
    print("The new basic is: ", new_basic)
    print("The new allowance is: ", new_allowance)
    print("The new PF is: ", new_pf)
    print("The new gratuity is: ", new_gratuity)
    print("The new CTC is: ", ctc)
    print("The new in-hand salary is: ", in_hand)

if __name__ == "__main__":
    main()