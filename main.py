import pandas as pd
from data_entry import get_date,get_transaction_id,get_transaction_details,get_date_optional,get_amount_optional,get_type_optional,get_description_optional
from tabulate import tabulate
import matplotlib.pyplot as plt
from database import add_transaction,get_transactions,create_transaction_table,delete_transaction,id_exists,update_transaction

def list_to_df(list_of_trans : list) -> pd.DataFrame:
    df = pd.DataFrame(list_of_trans,columns=["Trans_ID","Date","Amount","Type","Description"])
    df["Date"] = pd.to_datetime(df["Date"])
    return df

def print_transactions_table(transactions : list[tuple]) -> None:
    if not transactions:
        print("No transactions to display!")
        return
    
    formatted_rows = [
        (t[0], t[1], f"Rs. {t[2]:.2f}", t[3].capitalize(), t[4] or "N/A")
        for t in transactions
    ]
    print(
        tabulate(
            formatted_rows,
            headers=("Trans_ID","Date","Amount","Type","Description"),
            tablefmt="rounded_outline"
        )
    )

def plot_transactions(df : pd.DataFrame) -> None:
    plot_df = df.set_index("Date").sort_index()
    start=plot_df.index.min()
    end=plot_df.index.max()
    if start == end:
        start -= pd.Timedelta(days=1)
        end += pd.Timedelta(days=1)
    all_dates = pd.date_range(start,end,freq='D')

    income_df = (
        plot_df[plot_df["Type"]=='credit'] ["Amount"]
        .resample('D')
        .sum()
        .reindex(all_dates,fill_value=0)
        )
    expense_df = (
        plot_df[plot_df["Type"]=='debit'] ["Amount"]
        .resample('D')
        .sum()
        .reindex(all_dates,fill_value=0)
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
    id = add_transaction(*get_transaction_details())
    print(f"Transaction added successfully ! Transaction ID : {id}")
    
def transactions() ->None:
    start_date = get_date("Please enter the start date for the range (Leave blank for today's date) : ",True)
    end_date = get_date("Please enter the end date for range (Leave blank for today's date) : ",True)

    if start_date>end_date:
        print("Error : Start date cannot be after end date.")
        return

    list_of_trans = get_transactions(start_date,end_date)
    print_transactions_table(list_of_trans)
    if not list_of_trans:
        return
      
    df = list_to_df(list_of_trans)
    total_income = df[df["Type"] == "credit"]["Amount"].sum()
    total_expense = df[df["Type"] == "debit"]["Amount"].sum()
    print("\nSummary :")
    print(f"Total Income in the timeframe: Rs.{total_income:.2f}")
    print(f"Total Expenses in the timeframe: Rs.{total_expense:.2f} \n")
    print(f"Net Savings in the timeframe: Rs.{total_income-total_expense:.2f} \n")
    if input("Do you wish to see graph for the above transactions? (Y/N) : ").lower() == 'y':
        plot_transactions(df)

def delete() -> None:
    del_id = get_transaction_id("Enter the transaction ID you wish to delete: ")
    success =  delete_transaction(del_id)
    if success:
        print(f"Transaction ID {del_id} deleted successfully")
    else:
        print(f"Transaction ID {del_id} not found")

def get_by_id() -> None:
    i = get_transaction_id()
    transaction = id_exists(i)
    if not transaction:
        print("Provided transaction ID doesn't exist")
    else:
        print_transactions_table([transaction])

def update():
    while True:
        i = get_transaction_id("Enter the transaction ID to update (or 0 to cancel): ",allow_zero=True)
        if i == 0:
            print("Update cancelled")
            return
        record =  id_exists(i)
        if record:
            break
        print(f"Transaction ID {i} doesn't exist. Please try again.")

    _,curr_date,curr_amt,curr_type,curr_desc = record

    print(f"\n--- Updating Transaction #{i} ---")
    print("Press [Enter] on any field to keep the current value.\n")
    new_date = get_date_optional(curr_date)
    new_amount = get_amount_optional(curr_amt)
    new_type = get_type_optional(curr_type)
    new_desc = get_description_optional(curr_desc)
    if update_transaction(i,new_date,new_amount,new_type,new_desc):
        print(f"Transaction ID {i} updated successfully")
    else:
        print(f"Failed to update Transaction ID {i}.")
    
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
                cont = False
            case _:
                print("Please enter a valid choice : ")
        if cont:
            cont = input("Continue? (Y/N): ").lower() == 'y'
    print("Thank you for using the Expense Tracker... Exiting now ...")

if __name__ == "__main__" :
    main()