import tkinter as tk
from tkinter import messagebox


root = tk.Tk()
root.title("Expense Tracker Pro")
root.geometry("550x650")
root.config(bg="#1e1e2f")

expenses = []
budget_limit = 5000



def add_expense():
    name = name_entry.get().strip()
    amount = amount_entry.get().strip()
    category = category_var.get()

    if name == "" or amount == "":
        messagebox.showerror("Error", "Please fill all fields")
        return

    if not amount.isdigit():
        messagebox.showerror("Error", "Amount must be a number")
        return

    expense = f"{name} | {category} | ₹{amount}"
    expenses.append(expense)

    listbox.insert(tk.END, expense)

    with open("data.txt", "a") as file:
        file.write(expense + "\n")

    name_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)


def show_total():
    total = 0
    for item in expenses:
        amt = int(item.split("₹")[1])
        total += amt

    total_label.config(text=f"Total: ₹{total}")
    check_budget(total)


def check_budget(total):
    if total > budget_limit:
        messagebox.showwarning("Warning", "You exceeded your budget!")


def category_total():
    totals = {}

    for item in expenses:
        parts = item.split(" | ")
        category = parts[1]
        amount = int(parts[2].replace("₹", ""))

        totals[category] = totals.get(category, 0) + amount

    result = ""
    for cat, amt in totals.items():
        result += f"{cat}: ₹{amt}\n"

    messagebox.showinfo("Category Wise Spending", result)


def delete_expense():
    try:
        selected = listbox.curselection()[0]
        listbox.delete(selected)
        expenses.pop(selected)
        save_all_data()
    except:
        messagebox.showerror("Error", "Select an item to delete")


def clear_all():
    confirm = messagebox.askyesno("Confirm", "Clear all expenses?")
    if confirm:
        listbox.delete(0, tk.END)
        expenses.clear()
        save_all_data()
        total_label.config(text="Total: ₹0")


def search_expense():
    keyword = search_entry.get().lower()
    listbox.delete(0, tk.END)

    for item in expenses:
        if keyword in item.lower():
            listbox.insert(tk.END, item)


def export_csv():
    with open("expenses.csv", "w") as file:
        file.write("Name,Category,Amount\n")

        for item in expenses:
            parts = item.split(" | ")
            name = parts[0]
            category = parts[1]
            amount = parts[2].replace("₹", "")

            file.write(f"{name},{category},{amount}\n")

    messagebox.showinfo("Success", "Exported to expenses.csv")


def save_all_data():
    with open("data.txt", "w") as file:
        for item in expenses:
            file.write(item + "\n")


def load_data():
    try:
        with open("data.txt", "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    expenses.append(line)
                    listbox.insert(tk.END, line)
    except:
        pass



tk.Label(root, text="Expense Tracker Pro",
         font=("Segoe UI", 18, "bold"),
         bg="#1e1e2f", fg="white").pack(pady=10)

# Input Frame
input_frame = tk.Frame(root, bg="#2c2c3e", padx=10, pady=10)
input_frame.pack(pady=10, fill="x", padx=20)

tk.Label(input_frame, text="Expense Name", bg="#2c2c3e", fg="white").grid(row=0, column=0, sticky="w")
name_entry = tk.Entry(input_frame, width=30)
name_entry.grid(row=0, column=1, pady=5)

tk.Label(input_frame, text="Amount", bg="#2c2c3e", fg="white").grid(row=1, column=0, sticky="w")
amount_entry = tk.Entry(input_frame, width=30)
amount_entry.grid(row=1, column=1, pady=5)

tk.Label(input_frame, text="Category", bg="#2c2c3e", fg="white").grid(row=2, column=0, sticky="w")
category_var = tk.StringVar()
category_var.set("Food")

categories = ["Food", "Travel", "Shopping", "Bills", "Other"]
category_menu = tk.OptionMenu(input_frame, category_var, *categories)
category_menu.config(width=20)
category_menu.grid(row=2, column=1, pady=5)

# Buttons
btn_frame = tk.Frame(root, bg="#1e1e2f")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", command=add_expense,
          bg="#4CAF50", fg="white", width=10).grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="Total", command=show_total,
          bg="#2196F3", fg="white", width=10).grid(row=0, column=1, padx=5)

tk.Button(btn_frame, text="Category", command=category_total,
          bg="#9C27B0", fg="white", width=10).grid(row=0, column=2, padx=5)

# Search
search_entry = tk.Entry(root)
search_entry.pack(pady=5)

tk.Button(root, text="Search", command=search_expense,
          bg="#607D8B", fg="white").pack()

# Listbox
list_frame = tk.Frame(root)
list_frame.pack(pady=10)

listbox = tk.Listbox(list_frame, width=60, height=12)
listbox.pack(side=tk.LEFT)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Action Buttons
action_frame = tk.Frame(root, bg="#1e1e2f")
action_frame.pack(pady=10)

tk.Button(action_frame, text="Delete",
          command=delete_expense,
          bg="#f44336", fg="white", width=12).grid(row=0, column=0, padx=5)

tk.Button(action_frame, text="Clear All",
          command=clear_all,
          bg="#ff9800", fg="white", width=12).grid(row=0, column=1, padx=5)

tk.Button(action_frame, text="Export CSV",
          command=export_csv,
          bg="#00bcd4", fg="white", width=12).grid(row=0, column=2, padx=5)

# Total Label
total_label = tk.Label(root, text="Total: ₹0",
                       font=("Segoe UI", 14, "bold"),
                       bg="#1e1e2f", fg="#00e676")
total_label.pack(pady=10)

# Load saved data
load_data()

root.mainloop()