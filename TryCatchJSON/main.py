from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    # random choice with list comprehension
    password_list += [random.choice(LETTERS) for _ in range(nr_letters)]
    password_list += [random.choice(NUMBERS) for _ in range(nr_symbols)]
    password_list += [random.choice(SYMBOLS) for _ in range(nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showerror("Error", "Please enter all fields")
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file) # json file to dict
        except FileNotFoundError:
            print("data.json file not found. Create one.")
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            print("data.json file exist")
            # Update the data and then dump
            data.update(new_data)
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        finally:
            # Cleanup
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- SEARCH PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    if len(website) == 0:
        messagebox.showerror("Error", "Please enter all fields")
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file) # json to dict
        except FileNotFoundError:
            messagebox.showerror("Error", "No Data File Found.")
        else:
            if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo("website", f"Email: {email}\nPassword: {password}")
            else:
                messagebox.showerror("Error", f"No details for the {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #
########## Create a window ##########
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

########## Canvas ##########
canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

########## Labels ##########
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

########## Button ##########
generate_button = Button(text="Generate Password", width=12, command=generate_password)
generate_button.grid(row=3, column=2)

add_button = Button(text="Add", width=33, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=12, command=find_password)
search_button.grid(row=1, column=2)

########## Entry Box ##########
website_entry = Entry(width=19)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "dummy@gmail.com")

password_entry = Entry(width=19)
password_entry.grid(row=3, column=1)


# Keep the window open
window.mainloop()