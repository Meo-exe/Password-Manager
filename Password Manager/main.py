import json
from tkinter import *
import random
import pyperclip
from tkinter import messagebox


website = ""
email = ""
password = ""
# ---------------------------- CHECK WEBSITE ------------------------------- #
#
def check_website():
    website = website_entry.get()

    try:
        with open('data.json') as data_file:
            #reading old data
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror("No Data", "No data found")
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(website,
                                f"Website is already registered.\nEmail: {email}\nPassword: {password}")
            pyperclip.copy(password)
        elif len(website) == 0:
            messagebox.showerror("No Website Provided", "No Website Provided")
        else:
            messagebox.showinfo("Error", f"No information registered for {website}.")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate():
    global password
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    for char in range(nr_letters):
        password_list.append(random.choice(letters))

    for char in range(nr_symbols):
        password_list += random.choice(symbols)

    for char in range(nr_numbers):
        password_list += random.choice(numbers)

    random.shuffle(password_list)

    password = ""
    for char in password_list:
        password += char

    password_entry.insert(0,password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_password():
    global website, password, email
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Error", message="Please fill all fields")

    try:
        with open('data.json', "r") as data_file:
            #reading old data
            data = json.load(data_file)
            #updating old data
            data.update(new_data)
        with open("data.json", "w") as data_file:
            #saving new data
            json.dump(data, data_file, indent=4)
            password_entry.delete(0, END)


    #If there is no .json file, create one and write the first entry.
    except FileNotFoundError:
        with open(f"data.json", "w") as data_file:
            json.dump(new_data, data_file, indent=4)

            password_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50,pady= 50)

canvas = Canvas(width=200, height=200)
lock_pic = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_pic)
canvas.grid(row= 0, column= 1)


#Label
website_text = Label(text="Website:")
website_text.grid(row=1,column=0)
password = Label(text="Password:")
password.grid(row=3, column=0 )
email_username = Label(text="Email/Username:")
email_username.grid(row=2,column=0)


#Entries
email_entry = Entry(width=30)
email_entry.insert(0,"desaulnierse@gmail.com")
email_entry.grid(row=2,column=1)
website_entry = Entry(width=30)
website_entry.grid(row=1,column=1)
website_entry.focus()
password_entry = Entry(width=30)
password_entry.grid(row=3 , column=1)





#button
gen_button = Button(text = "Generate Password", command = generate)
add_button = Button(text = "Add", width = 36, command = save_password)
gen_button.grid(column=2, row=3)
add_button.grid(column=1, row=4, columnspan=2)
check_website = Button(text = "Search",  command = check_website)
check_website.grid(column=2, row=1)







window.mainloop()