def calculate_salary(base_value, current_bonus, percent_increase):
    new_basic = base_value + int(base_value * (percent_increase / 100))
    new_allowance = int(new_basic) * 0.63 + int(current_bonus)
    new_pf = int(new_basic) * 0.12
    new_gratuity = int(new_basic) * 0.05
    new_salary = int(new_basic) + int(new_allowance) + int(new_pf) + int(new_gratuity)
    ctc = int(new_salary) * 12
    in_hand = int(new_basic) + int(new_allowance) - int(new_pf)
    return new_salary, new_basic, new_allowance, new_pf, new_gratuity, new_salary, ctc, in_hand