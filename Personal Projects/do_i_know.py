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


def show_info(info_list):
    for name in info_list:
        print(f"-{name}")


def display_contacts(address_book):
    system("cls")
    for contact in range(0, len(address_book)):
        print(
            f"{contact+1} | Name: {address_book[contact][0]} {address_book[contact][1]}"
        )
    input(">>")


def backwards_adding():
    # Here the order im thinking but im feeling too lazy rn

    # take list as input, and use the length to determine what step its in, if len = 1
    # Youre at the second step, ie last name

    # use.pop() to just get rid of the last one, and then just return
    # and make sure the variable assigned to this function replaces
    # the existing list

    # Thats it, and then just do it over again for each step, but where you take input again
    # IDK how to handle going back mutiple times
    pass


# Apologies for the shit ton of repeating code, I don't know how to do this better :'(
def add_contact(address_book: list) -> list:

    print("To skip any of the field entries, just enter 'skip'")
    input_info = []

    print("Enter first name:")
    fName = input().strip()
    if fName.lower().strip() == "skip":
        fName = None

    input_info.append(fName)
    system("cls")

    show_info(input_info)
    print("Enter last name:")
    lName = input().strip()
    if lName.lower().strip() == "skip":
        lName = None

    input_info.append(lName)
    system("cls")

    show_info(input_info)
    print("Enter address:")
    address = input().strip()
    if address.lower().strip() == "skip":
        address = None

    input_info.append(address)
    system("cls")

    show_info(input_info)
    print("Enter phone number (no dashes or spaces):")
    phone = input().strip()
    if phone.lower().strip() == "skip":
        phone = None

    input_info.append(phone)
    system("cls")

    show_info(input_info)
    print("Enter email address:")
    email = input().strip()
    if email.lower().strip() == "skip":
        email = None

    input_info.append(email)
    system("cls")

    adding_contact = [fName, lName, address, phone, email]
    address_book.append(adding_contact)

    with open("contactos.pickle", "wb") as writer:
        dump(address_book, writer)

    print(f"Added {adding_contact[0]} to Address Book!")
    loading()


def edit_contact(address_book):
    repeat = False
    num_repeats = 0

    system("cls")
    print(
        heading + "Type first name of desired contact, otherwise type 'show contacts'"
    )
    search = input(">>").lower()
    search = search.replace(" ", "")

    if search == "showcontacts":
        display_contacts(address_book)
        print("Type first name of desired contact")
        search = input(">>").lower().strip()

    for contact in address_book:
        if contact[0].lower() == search and repeat == False:
            edit_index = address_book.index(contact)
            repeat = True
            num_repeats += 1

        elif contact[0].lower() == search and repeat == True:
            num_repeats += 1

    if repeat == True:
        system("cls")
        print(
            heading
            + f"There are {num_repeats} contacts with that name, please enter last name or 'show contacts':"
        )
        input(">>")

    input()


def delete_contact():
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

    # remember to make all the command elif start with system('cls')
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

    elif commands == "show":
        system("cls")
        display_contacts(book)
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
