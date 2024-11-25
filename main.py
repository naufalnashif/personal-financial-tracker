import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_desc

class CSV:
    CSV_FILE = 'finance_data.csv'
    COLUMNS = ['date', 'amount', 'category', 'desc']
    DATE_FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv (cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError as e :
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, desc):

        new_entry = {
            'date': date,
            'amount': amount,
            'category': category,
            'desc': desc
        }

        with open(cls.CSV_FILE, "a", newline="") as csvfile :
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)

        print('Entry added successfully')
    
    @classmethod
    def get_transaction(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df['date'] = pd.to_datetime(df['date'], format=cls.DATE_FORMAT)
        start_date = datetime.strptime(start_date, cls.DATE_FORMAT)
        end_date = datetime.strptime(end_date, cls.DATE_FORMAT)

        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty :
            print('No transaction found in the given date range.')
        else :
            print(
                f'Transactions from {start_date.strftime(cls.DATE_FORMAT)} to {end_date.strftime(cls.DATE_FORMAT)}'
            )
            print(
                filtered_df.to_string(
                    index=False,
                    formatters= {
                        "date" : lambda x : x.strftime(cls.DATE_FORMAT)
                    }
                )
            )

            total_income = filtered_df[filtered_df['category'] == 'Income']['amount'].sum()
            total_expense = filtered_df[filtered_df['category'] == 'Expense']['amount'].sum()

            print("\nSummary: ")
            print(f"Total Income: Rp. {total_income:.2f}")
            print(f"Total Expense: Rp. {total_expense:.2f}")
            print(f"Net Savings: Rp. {(total_income - total_expense):.2f}")
        
        return filtered_df

def add():
    CSV.initialize_csv()
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", 
        allow_default=True
    )
    amount = get_amount()
    category = get_category()
    desc = get_desc()
    CSV.add_entry(date, amount, category, desc)

def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. New transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1" :
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy) or enter for today's date: ", allow_default= True)
            end_date = get_date("Enter the end date (dd-mm-yyyy) or enter for today's date: ", allow_default= True)
            df = CSV.get_transaction(start_date=start_date, end_date=end_date)
        elif choice == "3":
            print("Exiting..")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.")



if __name__ == "__main__":
    CSV.initialize_csv()
    main()
