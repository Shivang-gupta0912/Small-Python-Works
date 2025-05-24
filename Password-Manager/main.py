from tkinter import messagebox
from tkinter import *
from random import randint, shuffle
import pyperclip
import json
from json.decoder import JSONDecodeError

# ---------------------------- SEARCH FUNCTION ---------------------------------- #

def search():
    website = website_entry.get()
    if len(website) == 0:
        messagebox.showinfo(title = "Oops", message = "Write website name to search!")
    else:
        try:
            with open("PasswordBook.json", mode = "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("PasswordBook.json", mode = "w") as data_file:
                messagebox.showinfo(title = "Oops", message = "No Result Found!")
        except JSONDecodeError:
            ''' if file exist but empty'''
            messagebox.showinfo(title = "Oops", message="No Result Found!")
        else:
            if website.lower() in data:
                username = data[website.lower()]["username"]
                password = data[website.lower()]["password"]
                messagebox.showinfo(title = f"{website}", message = f"Email/Username: {username}\nPassword: {password}")
                pyperclip.copy(password)
            else:
                messagebox.showinfo(title = "Oops", message = "No Result Found!")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = randint(8,10)
    symbols = randint(2,4)
    numbers = randint(2,4)

    string_of_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    list_of_symbols = ["!", "@", "#", "$", "&"]

    random_letters = [string_of_letters[randint(0, 51)] for _ in range(letters)]
    random_symbols = [list_of_symbols[randint(0, len(list_of_symbols)-1)] for _ in range(symbols)]
    random_numbers = [str(randint(0, 9)) for _ in range(numbers)]

    password = random_numbers+random_symbols+random_letters
    shuffle(password)
    password = "".join(password)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    '''It saves the password into the PasswordBook'''
    website_name = website_entry.get()
    username = email_username_entry.get()
    password = password_entry.get()
    new_data = {website_name.lower(): {
        "username": username,
        "password": password
    }}
    try:
        with open("PasswordBook.json", mode="r") as data_file:
            data = json.load(data_file)
            data.update(new_data)  # update method used in python dictionary
        with open("PasswordBook.json", mode="w") as data_file:
            json.dump(data, data_file, indent=4)
    except FileNotFoundError:
        with open("PasswordBook.json", mode="w") as data_file:
            json.dump(new_data, data_file, indent=4)
    except JSONDecodeError:
        '''This error occur when the file exist but empty'''
        with open("PasswordBook.json", mode="w") as data_file:
            json.dump(new_data, data_file, indent=4)
    finally:
        website_entry.delete(0, END)
        password_entry.delete(0, END)

def check_website():
    '''this function checks the existence of website in PasswordBook'''
    website = website_entry.get()
    try:
        with open("PasswordBook.json", mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        return False
    except JSONDecodeError:
        ''' if file exist but empty'''
        return False
    else:
        if website.lower() in data:
            return True
        else:
            return False

def add_password():
    website_name = website_entry.get()
    username = email_username_entry.get()
    password = password_entry.get()
    if website_name == "" or username == "" or password == "":
        messagebox.showinfo(title = "Oops", message = "Some fields are empty!")
    else:
        if check_website():
            do_change = messagebox.askokcancel(title = f"{website_name} exist", message = "Do You want change the password?")
            if do_change:
                save_password()
            else:
                pass
        else:
            is_ok = messagebox.askokcancel(title = website_name, message = f"These are the details entered: \nEmail/Username: {username}\nPassword: {password}\nIs it ok to save?")
            if is_ok:
                save_password()
            else:
                pass
# ---------------------------- DELETE PASSWORD ------------------------ #
def delete_record():
    website_name = website_entry.get()
    if website_name == "" :
        messagebox.showinfo(title = "Oops", message = "Some fields are empty!")
    else:
        if check_website():
            are_u_sure = messagebox.askyesno(title = "Delete Box", message = "Are You Sure?")
            if are_u_sure:
                #delete record
                with open("PasswordBook.json", "r") as data_file:
                    data = json.load(data_file)
                data.pop(f"{website_name}")
                with open("PasswordBook.json", mode = "w") as data_file:
                    json.dump(data, data_file, indent = 4)
                website_entry.delete(0, END)
            else:
                pass
        else:
            messagebox.showinfo(title = "Oops", message = "No Records!")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx = 50, pady = 50)

lock_img = PhotoImage(file = "logo.png")
canvas = Canvas(height = 200, width = 200)
canvas.create_image(100, 100, image = lock_img)
canvas.grid(row = 0, column = 1)

# Label
website_label = Label(text= "Website: ")
website_label.grid(row = 1, column = 0)

email_username_label = Label(text = "Email/Username: ")
email_username_label.grid(row = 1, column = 1)

password_label = Label(text = "Password: ")
password_label.grid(row = 1, column = 2)

# Entries
website_entry = Entry(justify="center",width = 25)
website_entry.focus()
website_entry.grid(row= 2, column = 0)

email_username_entry = Entry(width=35, justify="center")
email_username_entry.insert(END, "shivang.gupta0912@gmail.com")
email_username_entry.grid(row= 2, column = 1)

password_entry = Entry(width = 25, justify="center")
password_entry.grid(row = 2, column = 2)

# Buttons
generate_password_button = Button(text="Generate Password", command = password_generator, width= 21)
generate_password_button.grid(row = 3, column = 2)

add_button = Button(text = "Add", width = 51, command=add_password)
add_button.grid(row = 4, column = 1, columnspan = 2)

search_button = Button(text = "Search", width = 21,command = search)
search_button.grid(row = 3, column = 0)

delete_button = Button(text = "Delete", width = 21, command = delete_record)
delete_button.grid(row = 4, column = 0)

window.mainloop()