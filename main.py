from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)

    entry_password.delete(0, END)
    entry_password.insert(0, password)
    pyperclip.copy(password)
    # print(f"Your password is: {password}")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = entry_website.get()
    username = entry_username.get()
    password = entry_password.get()
    new_data = {
        website: {
            "email": username,
            "password": password,
        }
    }

    # Confirmation before saving
    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave any field empty")
    else:
        # is_ok = messagebox.askokcancel(title=f"{website}",
        #                                message=f"Here are the info to save: \n\nUsername :  {username}\n"
        #                                        f"Password:  {password}\n\nIs it ok to save?")
        # if is_ok:
        try:
            with open("data.json", "r") as file:
                # file.write(f"{website} ｜ {username} ｜ {password}\n")
                # TODO 1 : Handle the non english words
                # Function to write in a json. Open the file in "w" mode
                # json.dump(new_data, file, indent=4)
                # Function to read a json. It renders a dictionary. Open the file in "r" mode
                # data = json.load(file)
                # Function to append in a json. We have the load the old data first. Open the file in "r" mode
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            # We update the data
            data.update(new_data)
            # Then we have the open the file in "w" mode and write in it again
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            entry_website.delete(0, END)
            # entry_username.delete(0, END)
            entry_password.delete(0, END)


# --------------------------- FIND PASSWORD ---------------------------#
def find_password():
    # TODO 2: make the search not case sensitive
    website = entry_website.get()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showwarning(title="File Not Found", message="No Data File Found")
    else:
        if website in data:
            username = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title="Your credentials", message=f"Email/Username: {username}\n\nPassword: {password}")
        else:
            messagebox.showwarning(title="Website not found", message=f"No details for {website} exists")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Canvas
canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Labels
label_website = Label(text="Website: ")
label_website.config(width=20)
label_website.grid(column=0, row=1)
label_username = Label(text="Email/Username: ")
label_username.config(width=20)
label_username.grid(column=0, row=2)
label_password = Label(text="Password: ")
label_password.config(width=20)
label_password.grid(column=0, row=3)

# Entries
entry_website = Entry(width=21)
entry_website.focus()
entry_website.grid(column=1, row=1)
entry_username = Entry(width=40)
entry_username.insert(0, "james@bond.com")
entry_username.grid(column=1, row=2, columnspan=2)
entry_password = Entry(width=21)
entry_password.grid(column=1, row=3)

# Buttons
button_password = Button(text="Generate Password", width=15, command=generate_password)
button_password.grid(column=2, row=3)
button_add = Button(text="Add", width=38, command=save)
button_add.grid(column=1, row=4, columnspan=2)
button_search = Button(text="Search", width=15, command=find_password)
button_search.grid(column=2, row=1)

window.mainloop()
