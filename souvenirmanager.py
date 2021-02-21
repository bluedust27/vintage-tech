from souvenirs import Collectibles


def add_collectible():
    print()
    name = input("Name: ")
    collectible_type = input("Type: 1. Computer, 2. Camera, 3. Phone, 4. Video Player  ")
    date_manufactured = input("Manufacture date: ")
    description = input("Desc: ")
    Collectibles(name, collectible_type, date_manufactured, description)



def show_collectible():
    print()
    print("{0:10}\t{1:20}\t{2:20}".format("Name", "Date Manufactured", "Description"))
    for item in Collectibles.COLLECTIBLES_LIST:
        print("{0:10}\t{1:20}\t{2:20}".format(item.name, item.date_manufactured, item.description))



def delete_collectible():
    pass


def edit_collectible():
    pass


def show_menu():
    while True:
        print()
        print("1. Add collectible")
        print("2. Show")
        print("3. Delete")
        print("4. Edit")
        print("5. Exit")
        response = input("Choice: ")

        if response == "1":
            add_collectible()
        elif response == "2":
            show_collectible()
        elif response == "3":
            delete_collectible()
        elif response == "4":
            edit_collectible()
        elif response == "5":
            print("Exiting..")
            break
        else:
            print("Invalid")


show_menu()
