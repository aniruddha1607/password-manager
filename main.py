from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    password_list = []

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    generated_password = "".join(password_list)
    password_input.insert(0, generated_password)
    pyperclip.copy(generated_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

# f = open("password_details.json")


def add_details():
    website = website_input.get()
    password = password_input.get()
    email = email_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if website_input.index("end") != 0 and email_input.index("end") != 0 and password_input.index("end") != 0:

        is_ok = messagebox.askokcancel(title="confirm details",
                                       message=f"confirm password {password} for email {email} at site {website}"
                                               f"?")
        if is_ok:
            try:
                with open("password_details.json", "r") as data_file:
                    data = json.load(data_file)
                    data.update(new_data)

                with open("password_details.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)

            except FileNotFoundError:
                with open("password_details.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            website_input.delete(0, 'end')
            password_input.delete(0, 'end')

    else:
        messagebox.showerror(title="error", message="fields cannot be empty")


# ---------------------------- SEARCH PASSWORD ------------------------------- #

def search_password():
    website_name = website_input.get()

    try:
        with open("password_details.json", "r") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showerror(title="NO FILE", message="no database file present, please add a password to create file")

    else:
        if website_input.index("end") == 0:
            messagebox.showerror(title="ERROR", message="Please provide a website entry")
        else:
            try:
                password_input.delete(0, 'end')
                searched_email = data[website_name]["email"]
                searched_password = data[website_name]["password"]
                pyperclip.copy(searched_password)
                messagebox.showinfo(title="WEBSITE DETAILS", message=f"email:{searched_email}\npassword:"
                                                                     f"{searched_password}")
            except KeyError:
                messagebox.showinfo(title="NO ENTRY", message=f"no info for {website_name} present in database")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
psw_logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=psw_logo)
canvas.grid(column=2, row=1)

# website

website_label = Label(text="Website:", font=("Open Sans", 13, "bold"))
website_label.grid(column=1, row=2, pady=5, sticky="W")

website_input = Entry(width=36)
website_input.grid(column=2, row=2, columnspan=2, pady=5, sticky="W")
website_input.focus()

# email

email_label = Label(text="Email/Username:", font=("Open Sans", 13, "bold"))
email_label.grid(column=1, row=3, sticky="W")

email_input = Entry(width=35)
email_input.grid(column=2, row=3, columnspan=2, sticky="EW")

# password

password_label = Label(text="Password:", font=("Open Sans", 13, "bold"))
password_label.grid(column=1, row=4, pady=5, sticky="W")

password_input = Entry(width=30)
password_input.grid(column=2, row=4, pady=5, sticky="W")

generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=3, row=4, pady=5)

add_button = Button(text="Add", width=30, command=add_details)
add_button.grid(column=2, row=5, columnspan=2, sticky="EW")

# search button
generate_button = Button(text="Search", width=10, command=search_password)
generate_button.grid(column=3, row=2, sticky="E")

window.mainloop()
