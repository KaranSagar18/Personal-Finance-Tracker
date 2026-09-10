from datetime import datetime

date_format = "%d-%m-%Y"

def get_date(prompt , default_allowed = False):
    date_str = input(prompt)

    if default_allowed and not date_str:
        return datetime.today().strftime(date_format)

    try: 
        valid_date = datetime.strptime(date_str,date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid Date format. Please enter date in the format dd-mm-yyyy")
        return get_date (prompt, default_allowed)

def get_amount():
    try: 
        amount = float(input ( "Enter the amount : "))
        if amount <= 0 :
            raise ValueError ("Amount must be a non-negative and non-zero value")
        return amount
    except ValueError as e:
        print(e)
        get_amount() 

def get_date():
    pass

def get_date():
    pass