from datetime import datetime

DATE_FORMAT = "%d-%m-%Y"
DB_DATE_FORMAT = "%Y-%m-%d"
TRANS_TYPES = {
    "D" : "debit",
    "C" : "credit"
}

def get_date(prompt :str, default_allowed = False) -> str:
    while True:
        date_str = input(prompt).strip()

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
            amount = float(input ( "Enter the amount : ").strip())
            if amount <= 0 :
                raise ValueError ("Amount must be greater than zero.")
            return amount
        except ValueError as e:
            print(e)

def get_type() -> str:
    while True:
        transaction_type = input ( "Enter the type of transaction 'D' for debit(money spent) or 'C' for credit(money received) : " ).strip().upper()
        if transaction_type in TRANS_TYPES:
            return TRANS_TYPES[transaction_type]
        print("Invalid Transaction type.")

def get_description() -> str:
    desc = input("Enter the description for transaction (optional) : ").strip()
    return desc if desc else None

def get_transaction_id(
        prompt : str = "Enter the transaction ID : ",
        allow_zero : bool = False
) -> int:
    while True:
        try:
            val = int(input(prompt))
            if val == 0 and allow_zero:
                return 0
            if val <= 0:
                print("Transaction ID must be positive integer" + (" (or 0 to cancel)" if allow_zero else "."))
                continue
            return val
        except ValueError:
            print("Invalid ID!")

def get_transaction_details() -> tuple[str,float,str,str]:
    ask_date = "Enter transaction date (dd-mm-yyyy) or press 'enter' for today's date : "
    date = get_date(ask_date, True)
    amount = get_amount()
    transaction_type = get_type()
    description = get_description()
    return date,amount,transaction_type,description

def get_date_optional(curr_db_date : str) -> str:
    curr_display_date = datetime.strptime(curr_db_date,DB_DATE_FORMAT).strftime(DATE_FORMAT)
    while True:
        new_date = input(f"Enter new date (dd-mm-yyyy) [Press enter to keep {curr_display_date}] : ").strip()
        if not new_date:
            return curr_db_date
        try:
            valid_date = datetime.strptime(new_date,DATE_FORMAT)
            return valid_date.strftime(DB_DATE_FORMAT)
        except ValueError:
            print("Invalid date format, please enter date in format dd-mm-yyyy")

def get_amount_optional(curr_amt : float) -> float:
    while True:
        new_amt = input(f"Enter the new amount [Press enter to keep {curr_amt:.2f}]").strip()
        if not new_amt:
            return curr_amt
        try:
            amount = float(new_amt)
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
            return amount
        except ValueError as e:
            print(e)

def get_type_optional(curr_type : str) -> str:
    current_key = "D" if curr_type == "debit" else "C"
    while True:
        choice= input(f"Enter type 'D' for debit or 'C' for credit [Press enter to keep '{curr_type}'({current_key})]: ").strip().upper()
        if not choice:
            return curr_type
        if choice in TRANS_TYPES:
            return TRANS_TYPES[choice]
        print("Invalid Transaction type.")

def get_description_optional(curr_desc : str | None) -> str:
    disp_desc = curr_desc if curr_desc else "None"
    new_desc = input(f"Enter new description [Press enter to keep {disp_desc}] : ").strip()
    return new_desc if new_desc else curr_desc