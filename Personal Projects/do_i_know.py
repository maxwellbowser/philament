# Making CLI Address Book
from pickle import dump, load
from os import system
from time import sleep

heading = """
                 Address Book
-----------------------------------------------
"""
help_text = "For List of Commands, type 'help'"


def loading():
    sleep(1)
    print("Going back to main menu...")
    sleep(2.5)


# Apologies for the shit ton of repeating code, I don't know how to do this better :'(
def add_contact(address_book: list) -> list:

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
    address_book.append(adding_contact)
    with open("contactos.pickle", "wb") as writer:
        dump(address_book, writer)

    print(f"Added {adding_contact[0]} to Address Book!")
    loading()


def edit_contact(address_book):
    book_size = len(address_book)
    print(book_size)
    input()

    for list in address_book:
        print(f"Contact {list[0]}")

        print(address_book.index(list))

        if address_book.index(list) > 2:
            print("too many")
    input()


def delete_contact():
    pass


def show_contacts():
    pass


def reset_book(address_book):

    print(heading)
    print("Are you SURE that you want to delete the entire address book? (y\\n)")
    answer = input(">>").lower().strip()

    if answer != "y":
        return
    system("cls")

    print(heading)
    print("Type 'deleteAddressBook' to confirm (capitalization doesn't count):")
    answer = input(">>").lower().strip()

    if answer != "deleteaddressbook":
        return

    system("cls")
    print(heading)

    address_book = []
    with open("contactos.pickle", "wb") as writer:
        dump(address_book, writer)

    print("Address book has been cleared!")
    loading()


def search_contacts():
    pass


try:
    with open("contactos.pickle", "rb") as reader:
        book = load(reader)

except FileNotFoundError:
    book = []


# Running loop:
########################################################
while True:
    system("cls")
    print(heading + help_text)

    commands = input(">>").strip().lower()

    # remember to make all the commands start with system('cls')
    # just for consistencys sake!

    if commands == "add":
        add_contact(book)

    elif commands == "help":
        system("cls")
        print(
            """
Command List:
add -> add new contact
edit -> edit contact (WIP)
delete -> delete contact (WIP)
search -> search for contacts (WIP)
show -> display all contacts (WIP)
reset -> clear entire address book
exit -> exit program
"""
        )

        input("Hit enter to return to the main menu\n")

    elif commands == "edit":
        system("cls")
        edit_contact(book)

    elif commands == "exit":
        system("cls")
        print("Goodbye!")
        sleep(1)
        exit()

    elif commands == "reset":
        system("cls")
        reset_book(book)

    else:
        print("Sorry, that's not a command!")
        sleep(1)
