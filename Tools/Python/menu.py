def menu():
    print("[1] VCenter Info")
    print("[2] Option 2")
    print("[0] Exit the program.")

import connect

menu()
option = int(input("Enter your option: "))

while option != 0:
    if option == 1:
        print("VCenter Info Option Selected.")
        aboutInfo=si.content.about
        print(aboutInfo)
    elif option == 2:
        print("Option 2 Selected.")

    else:
        print("Invalid option.")

    print()
    menu()
    option = int(input("Enter your option: "))

print("Disconnecting, Goodbye.")