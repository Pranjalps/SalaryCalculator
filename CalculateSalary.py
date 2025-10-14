
from GetCurrentSalary import getCurrentSalary
def calculateSalary():
    """Calculate new salary based on given parameters."""
    
    # Load saved preset values if present

    baseValue, currentBonus, percentIncrease = getCurrentSalary()
    if baseValue is None or currentBonus is None or percentIncrease is None:
        print("Error: Missing salary parameters.")
        return



    newBasic = baseValue + int(baseValue)* (percentIncrease/100)
    newAllowance = int(newBasic)*0.63 + int(currentBonus)
    newPF = int(newBasic)*0.12
    newGratuity = int(newBasic)*0.05
    newSalary = int(newBasic) + int(newAllowance) + int(newPF) + int(newGratuity)
    ctc = int(newSalary)*12
    inHand = int(newBasic) + int(newAllowance) - int(newPF)
    print("The new salary is: ", newSalary)
    print("The new basic is: ", newBasic)
    print("The new allowance is: ", newAllowance)
    print("The new PF is: ", newPF)
    print("The new gratuity is: ", newGratuity)
    print("The new CTC is: ", ctc)
    print("The new in-hand salary is: ", inHand)