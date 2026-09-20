from datetime import datetime

DATE_FORMAT = "%d-%m-%Y"
DB_DATE_FORMAT = "%Y-%m-%d"
TRANS_TYPES = {
    "D" : "debit",
    "C" : "credit"
}

def get_date(prompt :str, default_allowed = False) -> str:
    while True:
        date_str = input(prompt)

        if default_allowed and not date_str:
            return datetime.today().strftime(DB_DATE_FORMAT)
        try: 
            valid_date = datetime.strptime(date_str,DATE_FORMAT)
            return valid_date.strftime(DB_DATE_FORMAT)
        except ValueError:
            print("Invalid Date format. Please enter date in the format dd-mm-yyyy")

def get_amount() -> float:
    while True:
        try: 
            amount = float(input ( "Enter the amount : "))
            if amount <= 0 :
                raise ValueError ("Amount must be greater than zero.")
            return amount
        except ValueError as e:
            print(e)

def get_type() -> str:
    while True:
        transaction_type = input ( "Enter the type of transaction 'D' for debit(money spent) or 'C' for credit(money received) : " ).upper()
        if transaction_type in TRANS_TYPES:
            return TRANS_TYPES[transaction_type]
        print("Invalid Transaction type.")

def get_description() -> str:
    return input("Enter the description for transaction (optional) : ")