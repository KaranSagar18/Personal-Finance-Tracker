from datetime import datetime

DATE_FORMAT = "%d-%m-%Y"
TRANS_TYPES = {
    "D" : "debit",
    "C" : "credit"
}

def get_date(prompt , default_allowed = False) -> str:
    date_str = input(prompt)

    if default_allowed and not date_str:
        return datetime.today().strftime(DATE_FORMAT)

    try: 
        valid_date = datetime.strptime(date_str,DATE_FORMAT)
        return valid_date.strftime(DATE_FORMAT)
    except ValueError:
        print("Invalid Date format. Please enter date in the format dd-mm-yyyy")
        return get_date (prompt, default_allowed)

def get_amount() -> float:
    try: 
        amount = float(input ( "Enter the amount : "))
        if amount <= 0 :
            raise ValueError ("Amount must be a non-negative and non-zero value")
        return amount
    except ValueError as e:
        print(e)
        get_amount() 

def get_type() -> str:
    type = input ( "Enter the type of transaction 'D' for debit(money spent) or 'C' for credit(money received) : " ).upper()
    if type in TRANS_TYPES:
        return TRANS_TYPES[type]
    print("Invalid Transaction type.")
    return get_type()

def get_description() -> str:
    return input("Enter the description for transaction (optional) : ")