import pandas as pd
import csv
from datetime import datetime

class CSV:
    CSV_FILE = "Transactions.csv"
    COLUMNS = ["date", "amount" , "type" , "description"]
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns= cls.COLUMNS)
            df.to_csv( cls.CSV_FILE , index = False)

    @classmethod
    def add_transaction(cls, date , amount , type , description):
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



