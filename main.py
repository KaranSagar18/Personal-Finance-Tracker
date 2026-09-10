import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date,get_type,get_amount,get_description

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

    @classmethod
    def get_transactions (cls, start_date : str , end_date :str):
        df = pd.read_csv(CSV.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"],format=CSV.DATE_FORMAT)
        start_date = datetime.strptime(start_date,CSV.DATE_FORMAT)
        end_date = datetime.strptime(end_date,CSV.DATE_FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the specified date range")
        else:
            print(f"Transactions from {start_date.strftime(CSV.DATE_FORMAT)} to {end_date.strftime(CSV.DATE_FORMAT)} :")
            print (filtered_df.to_string(index=False, formatters= {"date" : lambda x : x.strftime(CSV.DATE_FORMAT)}))

        total_income = filtered_df[filtered_df["type"] == "credit"] ["amount"].sum()
        total_expense = filtered_df[filtered_df["type"] == "debit"] ["amount"].sum()

        print("\n Summary :")
        print(f"Total Income in the timeframe: Rs.{total_income:.2f}")
        print(f"Total Expenses in the timeframe: Rs.{total_expense:.2f}")


def add() -> None:
    CSV.initialize_csv
    ask_date = "Enter the date in the format 'dd-mm-yyyy' or press enter for today's date : "
    date = get_date(ask_date, True)
    amount = get_amount()
    type = get_type()
    description = get_description()
    CSV.add_transaction(date,amount,type,description)

CSV.get_transactions('01-08-2026','01-09-2026')


