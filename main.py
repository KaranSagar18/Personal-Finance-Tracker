import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date,get_type,get_amount,get_description
from tabulate import tabulate
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "Transactions.csv"
    COLUMNS = ["date", "amount" , "type" , "description"]
    DATE_FORMAT = '%d-%m-%Y'
    @classmethod
    def initialize_csv(cls) -> None:
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns= cls.COLUMNS)
            df.to_csv( cls.CSV_FILE , index = False)

    @classmethod
    def add_transaction(cls, date , amount , type , description) -> None:
        transaction = {
            "date" : date,
            "amount" : amount,
            "type" : type,
            "description" : description
        }

        with open(cls.CSV_FILE , 'a' , newline= "") as csv_file:
            writer = csv.DictWriter(csv_file , fieldnames= cls.COLUMNS)
            writer.writerow(transaction)
        print("New Transaction added succesfully!")
        print(tabulate([transaction] , headers="keys" , tablefmt="grid"))
        print()


    @classmethod
    def get_transactions (cls, start_date : str , end_date :str) -> pd.DataFrame:
        df = pd.read_csv(CSV.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"],format=CSV.DATE_FORMAT)
        start_date = datetime.strptime(start_date,CSV.DATE_FORMAT)
        end_date = datetime.strptime(end_date,CSV.DATE_FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]
        # filtered_df["date"] = filtered_df["date"].apply(lambda x : x.strftime(CSV.DATE_FORMAT))

        if filtered_df.empty:
            print("No transactions found in the specified date range")
        else:
            print(f"Transactions from {start_date.strftime(CSV.DATE_FORMAT)} to {end_date.strftime(CSV.DATE_FORMAT)} :")
            # print (filtered_df.to_string(index=False, formatters= {"date" : lambda x : x.strftime(CSV.DATE_FORMAT)}))
            print(
                tabulate(
                    filtered_df.assign(date= filtered_df["date"].dt.strftime(CSV.DATE_FORMAT)),
                    headers=CSV.COLUMNS,tablefmt="grid",showindex=False
                )
            )

        total_income = filtered_df[filtered_df["type"] == "credit"] ["amount"].sum()
        total_expense = filtered_df[filtered_df["type"] == "debit"] ["amount"].sum()

        print("\nSummary :")
        print(f"Total Income in the timeframe: Rs.{total_income:.2f}")
        print(f"Total Expenses in the timeframe: Rs.{total_expense:.2f} \n")
        return filtered_df

def plot_transactions(df : pd.DataFrame) -> None:
    df.set_index("date", inplace=True)

    income_df = (
        df[df["type"]=='credit'] ["amount"]
        .resample('D')
        .sum()
        )
    expense_df = (
        df[df["type"]=='debit'] ["amount"]
        .resample('D')
        .sum()
        )
    # print(income_df.to_string())
    plt.figure(figsize=(10,5))
    plt.plot(income_df.index, income_df, label='Income', color='g')
    plt.plot(expense_df.index, expense_df, label='Expense', color='r')
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income & Expense in the Time Range")
    plt.legend()
    plt.grid(True)
    plt.show()

def add() -> None:
    CSV.initialize_csv
    ask_date = "Enter transaction date (dd-mm-yyyy) or press 'enter' for today's date : "
    date = get_date(ask_date, True)
    amount = get_amount()
    type = get_type()
    description = get_description()
    CSV.add_transaction(date,amount,type,description)

def main():
    print("\nMake a choice by selecting the corresponding number : ")
    while True:
        print("1. Add a transaction.")
        print("2. View Transactions and a summary within a date range.")
        print("3. Exit.")
        choice = input("Enter your choice (1-3) : ").lstrip('0')

        if choice == '3':
            break
        elif choice == '1':
            add()
        elif choice == '2':
            df = CSV.get_transactions(
                get_date("Please enter the start date for the range (Leave blank for today's date) : ",True),
                get_date("Please enter the end date for range (Leave blank for today's date) : ",True)
                )
            if input("Do you wish to see the graph for the above transactions? (y/n) : ").lower() == 'y':
                plot_transactions(df)
        else: 
            print("Please enter a valid choice : ")

if __name__ == "__main__" :
    main()


