import csv
import os
from datetime import datetime

# CSV 檔案儲存位置
folder = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(folder, "expenses.csv")

# 如果 CSV 不存在，建立檔案並寫入標題
if not os.path.exists(filename):
    with open(filename, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "amount", "category", "notes"])

print("=== Expense Tracker ===")

while True:

    # 1. 輸入日期
    while True:
        date = input("Date (YYYY-MM-DD): ")

        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date! Please try again.")

    # 2. 輸入金額
    while True:
        try:
            amount = float(input("Amount: "))

            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")

        except ValueError:
            print("Please enter a valid number.")

    # 3. 輸入類別
    while True:
        category = input("Category: ").strip()

        if category:
            break

        print("Category cannot be empty.")

    # 4. 輸入備註（可留空）
    notes = input("Notes (optional): ")

    # 5. 儲存支出資料
    with open(filename, "a", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow([date, amount, category, notes])

    print("\nExpense saved successfully!\n")

    # 6. 是否繼續新增
    again = input("Add another expense? (y/n): ").strip().lower()

    if again != "y":
        break

print("Program finished.")