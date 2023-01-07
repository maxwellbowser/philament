# Making CLI Address Book
import pickle
from os import system
from time import sleep

# attempt number one

# Apologies for the shit ton of repeating code, I don't know how to do this better :'(
def add_contact(current_contacts: list) -> list:
    system("cls")
    print("To skip any of the field entries, just enter 'skip'")

    print("Enter first name:")
    fName = input().strip()
    if fName.lower().strip() == "skip":
        fName = None
    system("cls")

    print("Enter last name:")
    lName = input().strip()
    if lName.lower().strip() == "skip":
        lName = None
    system("cls")

    print("Enter address:")
    address = input().strip()
    if address.lower().strip() == "skip":
        address = None
    system("cls")

    print("Enter phone number (no dashes or spaces):")
    phone = input().strip()
    if phone.lower().strip() == "skip":
        phone = None
    system("cls")

    print("Enter email address:")
    email = input().strip()
    if email.lower().strip() == "skip":
        email = None
    system("cls")

    adding_contact = [fName, lName, address, phone, email]
    current_contacts.append(adding_contact)
    with open("contactos.pickle", "wb") as writer:
        pickle.dump(current_contacts, writer)

    print(f"Added {adding_contact[0]} to Address Book!")
    sleep(1)
    print("Going back to main menu...")
    sleep(2.5)


def edit_contact():
    pass


def delete_contact():
    pass


def show_contacts():
    pass


def reset_book():
    pass


def search_contacts():
    pass


try:
    with open("contactos.pickle", "rb") as reader:
        hello = pickle.load(reader)

except FileNotFoundError:
    hello = []

# Running loop:
while True:
    system("cls")
    print(
        """
                 Address Book
-----------------------------------------------
For List of Commands, type 'help'
"""
    )
    commands = input(">>").strip().lower()

    if commands == "add":
        add_contact(hello)

    elif commands == "help":
        system("cls")
        print(
            """
Command List:
add -> add new contact
edit -> edit contact
delete -> delete contact
search -> search for contacts
show -> display all contacts
reset -> clear entire address book
exit -> exit program
"""
        )

        input("Hit enter to return to main menu\n")

    elif commands == "exit":
        system("cls")
        print("Goodbye!")
        sleep(1)
        exit()

    else:
        print("sorry that's not a command, please enter help for a list of commands")
        sleep(3)
