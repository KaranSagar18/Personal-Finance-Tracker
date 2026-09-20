import pandas as pd
from data_entry import get_date,get_type,get_amount,get_description
from tabulate import tabulate
import matplotlib.pyplot as plt
from database import add_transaction,get_transactions,create_transaction_table,delete_transaction,id_exists,update_transaction

def list_to_df(list_of_trans : list) -> pd.DataFrame:
    df = pd.DataFrame(list_of_trans,columns=["Trans_ID","Date","Amount","Type","Description"])
    df["Date"] = pd.to_datetime(df["Date"])
    return df

def plot_transactions(df : pd.DataFrame) -> None:
    df.set_index("Date", inplace=True)
    df.sort_index(inplace=True)

    income_df = (
        df[df["Type"]=='credit'] ["Amount"]
        .resample('D')
        .sum()
        )
    expense_df = (
        df[df["Type"]=='debit'] ["Amount"]
        .resample('D')
        .sum()
        )

    plt.figure(figsize=(10,5))
    plt.plot(income_df.index, income_df, label='Income', color='g', marker='o')
    plt.plot(expense_df.index, expense_df, label='Expense', color='r', marker = 'o')
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income & Expense in the Time Range")
    plt.legend()
    plt.grid(True,linestyle="dashed")
    plt.show()

def add() -> None:
    ask_date = "Enter transaction date (dd-mm-yyyy) or press 'enter' for today's date : "
    date = get_date(ask_date, True)
    amount = get_amount()
    transaction_type = get_type()
    description = get_description()
    id = add_transaction(date,amount,transaction_type,description)
    print(f"Transaction added successfully ! Transaction ID : {id}")
    
def transactions():
    start_date = get_date("Please enter the start date for the range (Leave blank for today's date) : ",True)
    end_date = get_date("Please enter the end date for range (Leave blank for today's date) : ",True)
    list_of_trans = get_transactions(start_date,end_date)
    if not list_of_trans:
        print("No transactions to print!")
        return
    else:
        print(tabulate(list_of_trans,headers=("Trans_ID","Date","Amount","Type","Description")))
    df = list_to_df(list_of_trans)
    total_income = df[df["Type"] == "credit"]["Amount"].sum()
    total_expense = df[df["Type"] == "debit"]["Amount"].sum()
    print("\nSummary :")
    print(f"Total Income in the timeframe: Rs.{total_income:.2f}")
    print(f"Total Expenses in the timeframe: Rs.{total_expense:.2f} \n")
    print(f"Net Savings in the timeframe: Rs.{total_income-total_expense:.2f} \n")
    if input("Do you wish to see graph for the above transactions? (Y/N) : ").lower() == 'y':
        plot_transactions(df)

def delete():
    while True:
        try:
            del_id = int(input("Enter the transaction ID you wish to delete : "))
            break
        except ValueError:
            print("Enter a valid integer transaction ID : ")
    success =  delete_transaction(del_id)
    if success:
        print(f"Transaction ID {del_id} deleted successfully")
    else:
        print(f"Transaction ID {del_id} not found")

def get_by_id():
    while True:
        try:
            i = int(input("Enter the transaction ID : "))
            break
        except ValueError:
            print("Invalid ID!")
    transaction = id_exists(i)
    if not transaction:
        print("Provided transaction ID doesn't exist")
    else:
        print(tabulate(transaction,headers=["Trans_ID","Date","Amount","Type","Description"]))

def update():
    while True:
        try:
            i = int(input("Enter the transaction ID : "))
            if not id_exists(i):
                print("Provided transaction ID doesn't exist")
                continue
            break
        except ValueError:
            print("Invalid ID!")
    
    ask_date = "Enter transaction date (dd-mm-yyyy) or press 'enter' for today's date : "
    date = get_date(ask_date, True)
    amount = get_amount()
    transaction_type = get_type()
    description = get_description()
    if update_transaction(i,date,amount,transaction_type,description):
        print(f"Transaction ID {i} updated successfully")
    

def main():
    create_transaction_table()
    print("\nMake a choice by selecting the corresponding number : ")
    cont = True
    while cont:
        print("1. Add a transaction.")
        print("2. View Transactions and a summary within a date range.")
        print("3. Delete a transaction.")
        print("4. View transaction by ID.")
        print("5. Update transaction by ID.")
        print("6. Exit.")
        choice = input("Enter your choice (1-6) : ").lstrip('0')

        match choice:
            case '1':
                add()
            case '2':
                transactions()
            case '3':
                delete()
            case '4':
                get_by_id()
            case '5':
                update()
            case '6':
                print("Thank you for using the Expense Tracker... Exiting now ...")
                cont = False
            case _:
                print("Please enter a valid choice : ")
        if cont:
            cont = input("Continue? (Y/N): ").lower() == 'y'
    print("Thank you for using the Expense Tracker... Exiting now ...")

if __name__ == "__main__" :
    main()


