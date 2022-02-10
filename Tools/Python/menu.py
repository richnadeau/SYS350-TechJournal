def menu():
    print("[1] VCenter Info")
    print("[2] Session Details")
    print("[3] VM Details")
    print("[0] Exit the program.")

import connect
from pyVim.connect import Disconnect

menu()
option = int(input("Enter your option: "))

while option != 0:
    if option == 1:
        print("VCenter Info Option Selected.")
        aboutInfo=connect.si.content.about
        print(aboutInfo)
    elif option == 2:
        print("Session Details Selected.")
        for session in connect.si.content.sessionManager.sessionList:
            if session.key == connect.si.content.sessionManager.currentSession.key:
                print("~~~~~~~~~~~~~~~~~~~~~")
                print("username = {0.userName}".format(session))
                print("ip = {0.ipAddress}".format(session))
                print("vcenter host = ", connect.vcenterh)
                print("~~~~~~~~~~~~~~~~~~~~~")
    elif option == 3:
        print("VM Details Selected.")
        connect.si.RetrieveContent()
        datacenter = connect.si.content.rootFolder.childEntity[0]
        vms = datacenter.vmFolder.childEntity
        vmname=input("Enter the name of your VM (leave empty if you want all printed): ")

        if len(vmname) == 0:
            for i in vms:
                print("Name: ", i.name)
                print("State: ", i.guest.guestState)
                print("# of Processors: ", i.config.hardware.numCPU, " CPU(s)")
                GB = (i.config.hardware.memoryMB/1024)
                print("Memory Total: ", GB , " GB")
                print("IP Address: ", i.summary.guest.ipAddress)
                print("~~~~~~~~~~~~~~~~~~~~~") 
        else:
            for i in vms:               
                if vmname in str(i.name):
                    print("Name: ", i.name)
                    print("State: ", i.guest.guestState)
                    print("# of Processors: ", i.config.hardware.numCPU, " CPU(s)")
                    GB = (i.config.hardware.memoryMB/1024)
                    print("Memory Total: ", GB , " GB")
                    print("IP Address: ", i.summary.guest.ipAddress)
                    print("~~~~~~~~~~~~~~~~~~~~~")
                        
    else:
        print("Invalid option.")

    print()
    menu()
    option = int(input("Enter your option: "))

Disconnect(connect.si)
print("Disconnecting, Goodbye.")