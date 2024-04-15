#Discriptiom: Create Invoice For One Stop Insurace. 
#Name: Morgan Browne
#Date: March 17th 2024 
#Update: April 12-13, 2024 Updated and fixed Input for phone number and printing previous claims.


import datetime
import FormatValues as FV
import re
# Format for validating phone number 
pattern = re.compile(r'^\d{3}-\d{4}$')


def IsValidLetter(letter):
    ALLOWED_CHAR_SET = set("AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz-. '1234567890")
    return set(letter).issubset(ALLOWED_CHAR_SET)

def IsValidNum(name):
    ALLOWED_NUM_SET = set("1234567890-")
    return set(name).issubset(ALLOWED_NUM_SET)

def ValidatePostalCode(PostalCode, Country):
    postalCodePatterns = {
        "US": r"^\d{5}(?:-\d{4})?$",  # US ZIP codes (with optional +4 extension)
        "CA": r"^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$",  # Canadian postal codes
        # Add more patterns for other countries as needed
    }
    
    if Country in postalCodePatterns:
        pattern = postalCodePatterns[Country]
        return re.match(pattern, PostalCode) is not None
    else:
        return True  # Allow any input for unknown countries


def PaymentOptions():
    PAY_OPTIONS = ["Full", "Monthly", "Down Payment"]
    while True:
        PayOption = input("How is the customer paying (Full, Monthly, or Down Payment): ").title()
        if PayOption not in PAY_OPTIONS:
            print("Invalid option.")
        else:
            return PayOption

def MonthlyPay(TotalCost, DownPayment):
    if DownPayment > 0:
        TotalCost -= DownPayment
    MonthlyPayments = (TotalCost + PRO_FEE_PAYMENT) / 8
    return MonthlyPayments

def DownPayValidation(DownPay):
    if not DownPay.strip():  
        return False, "Input cannot be empty."

    if not DownPay.replace('.', '', 2).isdigit():
        return False, "Invalid input. Please enter a valid number for the down payment."

    DownPay = float(DownPay)
    if DownPay >= 0:
        return True, DownPay
    else:
        return False, "Down payment must be a positive number."""

PrevCusClaimLst = []

def PrevCusClaimInfo(PrevCusClaimLst):
    while True:
        PrevCusClaim = input("Does the customer have any previous claims? (Y or N): ").upper()
        if PrevCusClaim == "N":
            break
        elif PrevCusClaim != "Y":
            print("Data Entry Error - Must enter either Y or N.")
            continue
            
        PrevClaimNum = input("Enter the previous claim number: ")
        if not IsValidNum(PrevClaimNum):
            print("Data Entry Error - Must use a numerical value.")
            continue

        PrevClaimDate = input("Enter the previous claim date (YYYY-MM-DD): ")
        if not IsValidLetter(PrevClaimDate):
            print("Data Entry Error - must use correct date format.")
            continue

        PrevClaimAmnt = input("Enter the previous claim amount: ")
        if not IsValidNum(PrevClaimAmnt):
            print("Data Entry Error - must use numerical value.")
            continue

        PrevCusClaimLst.append((PrevClaimNum, PrevClaimDate, PrevClaimAmnt))
    return PrevCusClaimLst

# Bring over defaults for program
f = open('Defualt.dat', 'r')
POLICY_NUM = int(f.readline())
BASE_PREMIUM = float(f.readline())
DISS_CAR = float(f.readline())
LIABLE_COVER = float(f.readline())
GLASS_COVER = float(f.readline())
LOAN_COVER = float(f.readline())
HST_RATE = float(f.readline())
PRO_FEE_PAYMENT = float(f.readline())
f.close()
print()
print("Invoice For One Stop Insurace")
print()
while True: 
    # Gather user input
    while True: 
        FirstName = input("Enter the customer's first name: ").title()
        if FirstName == "":
            print("Data Entry Error - Customer First Name Cannot Be Blank.")
        elif not FirstName.isalpha():
            print("Data Entry Error - First Name Cannot Contain Numbers.")
        else:
            break

    while True:
        LastName = input("Enter the customer's last name: ").title()
        if LastName == "":
            print("Data Entry Error - Customer Last Name Cannot Be Blank.")
        elif not LastName.isalpha():
            print("Data Entry Error - Last Name Cannot Contain Numbers.")   
        else:
            break

    ProvLst = ["NL", "NS", "NB", "PE", "PQ", "ON", "MB", "AB", "BC", "NT", "YT", "NV"]
    while True:
        Prov = input("Enter the customer province (XX): ")
        if Prov == "":
            print("Error - cannot be blank.")
        elif len(Prov) != 2:
            print("Error - must be 2 characters only.")
        elif Prov not in ProvLst:
            print("Error - invalid province.")
        else:
            break

    while True:
        Address = input("Enter the customer's Address: ").title()
        if Address == "":
            print("Data Entry Error - Address Cannot Be Blank.")
        else:
            break

    while True:
        City = input("Enter the customer's City: ").title()
        if City == "":
            print("Data Entry Error - City Cannot Be Blank.")
        elif not City.isalpha(): # This is so the user cannot enter numbers, only problem is the city wont be able to have punctuation marks.
            print("Data Entry Error - City Cannot Contain Numbers.")
        else:
            break

    while True:
        PostCode = input("Enter the customer's Postal Code (A1A A1A): ").upper()
        
        # Check if the postal code is blank
        if PostCode == "":
            print("Data Entry Error - Postal Code Cannot Be Blank.")
            continue
        
        # Define a regular expression pattern for Canadian postal codes (A1A 1A1)
        pattern = r'^[A-Z]\d[A-Z] \d[A-Z]\d$'
        
        # Validate the format of the postal code
        if not re.match(pattern, PostCode):
            print("Data Entry Error - Invalid Postal Code Format. Please use format A1A 1A1.")
            continue
        
        # If the code passes all validations, break the loop
        break

    # April 12, 2024 fix this phone number validation at a later point
    # April 12, 2024 Fix the phone number validation used re to have user us sp format 
    while True:
        PhoneNum = input("Enter your phone number (format: XXX-XXXX): ")

        # Regular expression to match the format XXX-XXXX
        pattern = re.compile(r'^\d{3}-\d{4}$')

        if pattern.match(PhoneNum):
            # Removing non-numeric characters for counting digits
            cleaned_number = ''.join(filter(str.isdigit, PhoneNum))
            if len(cleaned_number) == 7:
                print("Valid phone number.")
                break  # Exit the loop since a valid phone number is entered
            else:
                print("Invalid phone number. Please enter a phone number with 7 digits after the hyphen.")
        else:
            print("Invalid phone number format. Please enter in the format XXX-XXXX.")

        # Old PhoneNum vlaidation 
        """if PhoneNum == "":
            print("Data Entry Error - Phone number cannot be blank.")
        elif len(PhoneNum) != 8:  # len() functions returns the length of a string.
            print("Data Entry Error - Phone number must be 10 digits only.")
        elif PhoneNum.isdigit() == False: # Isdigit() is a method that checks that all characters are digits.
            print("Data Entry Error - Phone number must be 10 digits only.")
        else:
            break"""
    

    while True:
        NumCars = input("Enter the number of cars being insured: ")
        NumCars = int(NumCars)
        if NumCars == "":
            print("Data Entry Error - Number Of Cars Cannot Be Blank.")
        else:
            break

    while True:
        InsurOpt = input("Extra Coverage up to $1,000,000 (Y or N): ").upper()
        if InsurOpt =="":
            print("Data Entry Error - Extra Coverage Cannot Be Blank.")
        else:
            break

    while True:
        GlassCover = input("Glass Coverage (Y or N): ").upper()
        if GlassCover =="":
            print("Data Entry Error - Glass Coverage Cannot Be Blank.")
        else:
            break

    while True:
        LoanCar = input("Loaner Car (Y or N): ").upper()
        if LoanCar == "":
            print("Data Entry Error - Loaner Car Cannot Be Blank.")
        else:
            break

    # Now, within the main loop, after gathering the customer's first name, we call PrevCusClaimInfo(PrevCusClaimLst) to prompt the user if there are any previous claims.
    PrevCusClaimLst = PrevCusClaimInfo(PrevCusClaimLst)


    # Calculations
    TotalCost = BASE_PREMIUM + (NumCars - 1) * (BASE_PREMIUM * DISS_CAR)
    AddedCosts = 0
    if InsurOpt == "Y":
        TotalCost += NumCars * LIABLE_COVER
        AddedCosts += NumCars * LIABLE_COVER
    if GlassCover == "Y":
        TotalCost += NumCars * GLASS_COVER
        AddedCosts += NumCars * GLASS_COVER
    if LoanCar == "Y":
        TotalCost  += NumCars * LOAN_COVER
        AddedCosts  += NumCars * LOAN_COVER

    HST = TotalCost * HST_RATE
    PayOption = PaymentOptions()

    while True:
        if PayOption == "Down Payment":
            while True:
                DownPay = input("Enter the amount the customer will pay down: ")
                try:
                    DownPay = float(DownPay)
                    if DownPay >= 0 and DownPay <= TotalCost:
                        break
                    else:
                        print("Data Entry Error - Down Payment must be between 0 and total cost.")
                except ValueError:
                    print("Data Entry Error - must enter a numeric value.")
        else:
            DownPay = 0
        break

    InsurePrem = TotalCost - HST

    if PayOption == 'Full':
        PayAmnt = TotalCost
        MonthlyPayments = 0.0
    else:
        PaymentAmnt = TotalCost + PRO_FEE_PAYMENT
        MonthlyPayments = MonthlyPay(TotalCost, DownPay)

    CurrentDate = datetime.datetime.now()
    InvoiceDate = CurrentDate.strftime("%Y-%m-%d")
    NextMonth = (CurrentDate + datetime.timedelta(days=31)).strftime("%Y-%m-%d")
    Year = CurrentDate.year + (CurrentDate.month // 12)                                    
    Month = 1 if CurrentDate.month == 12 else CurrentDate.month + 1
    NextMonth = datetime.datetime(Year, Month, 1).strftime("%Y-%m-%d")
    FirstPaymentDate = NextMonth
    NumCarsDsp = str(NumCars)

    if PayOption == "Full":
        PayOptionDsp = "Paid In Full"
    elif PayOption == "Monthy":
        PayOptionDsp = "Monthly Payments"
    else:
        PayOptionDsp = "Down Payment"
    
    # Add the first and last name together to save space. 
    WholeName = FirstName + " " + LastName

    # Print results 
    print()
    print("         1         2         3         4         5")
    print("12345678901234567890123456789012345678901234567890")
    print()
    print("-----------------------------------------------------")
    print("One Stop Insurance                Customer Invoice")
    print()
    print(f"Policy #{POLICY_NUM:<5}")
    print("-----------------------------------------------------")
    print("Customer Information:                             ")
    print()
    print(f"Name:     {WholeName:<20s}Phone Number: {PhoneNum:<10s}     ")
    print(f"Address:  {Address:<20s}                           ")
    print(f"City:     {City:<15s}                                 ")
    print(f"Provence: {Prov:<2s}                    Postal Code: {PostCode:<7s}                   ")
    print("-----------------------------------------------------")
    print("Options:                                          ")
    print()
    print(f"Number Of Cars:  {NumCars:<2d}                     ")
    print(f"Extra Liability: {InsurOpt:<2s}                    ")
    print(f"Glass Coverage:  {GlassCover:<2s}                  ")
    print(f"Loaner Car:      {LoanCar:<2s}                         ")
    print("-----------------------------------------------------")
    print("Payment Information:                              ")
    print()
    print(f"Date Of Invoice:                  {InvoiceDate:<10s}")
    print(f"First Payent Starts:              {FirstPaymentDate:<10s}")
    print()
    print(f"Payment Type:                     {PayOptionDsp:<15s}")
    print(f"Down Payment Amount:              {FV.FDollar2(DownPay)}")
    print(f"Monthly Payment:                  {FV.FDollar2(MonthlyPayments)}")
    print(f"Added Costs:                      {FV.FDollar2(AddedCosts)}")
    print(f"Insurance Premium:                {FV.FDollar2(InsurePrem)}")
    print(f"HST:                              {FV.FDollar2(HST)}")
    print(f"Total:                            {FV.FDollar2(TotalCost)}")
    print("-----------------------------------------------------")
    # Display previous claims
    print("Customer Previous Claim(s):")
    print()
    print("Claim #          Claim Date         Amount")
    print("-----------------------------------------------------")
    for claim in PrevCusClaimLst:
        print(f"{claim[0]:<10}       {claim[1]:<12}      {FV.FDollar2(float(claim[2]))}")
    print("-----------------------------------------------------")

    POLICY_NUM += 1
    print("Policy Data Has Been Saved.")
    print()
    if input("Do you want to enter another customer? (Y/N): ").upper() != 'Y':
        break

    # Housekeeping 
    # Default values back to defaults.dat
    f = open('defualts.dat', 'w')
    f.write("{}/n".format(str(POLICY_NUM)))
    f.write("{}/n".format(str(BASE_PREMIUM)))
    f.write("{}/n".format(str(DISS_CAR)))
    f.write("{}/n".format(str(LIABLE_COVER)))
    f.write("{}/n".format(str(GLASS_COVER)))
    f.write("{}/n".format(str(LOAN_COVER)))
    f.write("{}/n".format(str(HST_RATE)))
    f.write("{}/n".format(str(PRO_FEE_PAYMENT)))
    f.close()
