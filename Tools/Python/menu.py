# Author of the this Python Script: richnadeau
def menu():
    print("[1] VCenter Info")
    print("[2] Session Details")
    print("[3] VM Details")
    print("[4] VM Actions")
    print("[0] Exit the program.")

def vmmenu():
    print("[1] Power on VM")
    print("[2] Power Off VM")
    print("[3] Take a Snapshot")
    print("[4] Delete a VM")
    print("[5] Reconfigure a VM")
    print("[6] Change a VM's Network")
    print("[0] Exit the VM Actions.")

from time import sleep
import connect
from pyVim.connect import Disconnect
from pyVmomi import vim

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
    elif option == 4:
        vmmenu()
        vmoption = int(input("Enter your option: "))
        
        while vmoption != 0:
            if vmoption == 1:
                print("You Have Chosen to Power on VM(s)")
                connect.si.RetrieveContent()
                datacenter = connect.si.content.rootFolder.childEntity[0]
                vms = datacenter.vmFolder.childEntity
                poweronname=input("Enter the name of your VM that you want powered on (leave empty if you want all powered on): ")
                
                if len(poweronname) == 0:
                    for i in vms:
                        if i.guest.guestState == "running":
                            print(i.name, " is already powered on, skipping!")
                        else:
                            print(i.name, " is not powered on, powering on now!")
                            i.PowerOn()

                else:
                    for i in vms:               
                        if poweronname in str(i.name):
                            if i.guest.guestState == "running":
                                print(i.name, " is already powered on, skipping!")
                            else:
                                print(i.name, " is not powered on, powering on now!")
                                i.PowerOn()


            elif vmoption == 2:
                print("You Have Chosen to Power off VM(s)")
                connect.si.RetrieveContent()
                datacenter = connect.si.content.rootFolder.childEntity[0]
                vms = datacenter.vmFolder.childEntity
                poweroffname=input("Enter the name of your VM that you want powered off (leave empty if you want all powered on): ")
                
                if len(poweroffname) == 0:
                    for i in vms:
                        if i.guest.guestState == "notRunning":
                            print(i.name, " is already powered off, skipping!")
                        else:
                            print(i.name, " is not powered off, powering off now!")
                            i.PowerOff()

                else:
                    for i in vms:               
                        if poweroffname in str(i.name):
                            if i.guest.guestState == "notRunning":
                                print(i.name, " is already powered off, skipping!")
                            else:
                                print(i.name, " is not powered off, powering off now!")
                                i.PowerOff()

            elif vmoption == 3:
                print("You Have Chosen to take a Snapshot of a VM")
                connect.si.RetrieveContent()
                datacenter = connect.si.content.rootFolder.childEntity[0]
                vms = datacenter.vmFolder.childEntity
                snapshotvmname=input("Enter the name of the VM you want to take a snapshot of: ")

                for i in vms:
                    if snapshotvmname in str(i.name):
                        selection=input(i.name + " is selected, are you sure you want to take a snapshot of this VM? (Y/N): ")
                        if selection == "Y":
                            naming=input("What would you like to name this snapshot? ")
                            print("Taking a snapshot of ", i.name, " called ", naming)
                            i.CreateSnapshot_Task(name=naming, description=None, memory=True, quiesce=False)
                            print()
                        elif selection == "N":
                            print()

            elif vmoption == 4:
                print("You Have Chosen to Delete VM(s)")
                connect.si.RetrieveContent()
                datacenter = connect.si.content.rootFolder.childEntity[0]
                vms = datacenter.vmFolder.childEntity
                delvmname=input("Enter the name of the VM you want to delete: ")

                for i in vms:
                    if delvmname in str(i.name):
                        selection=input(i.name + " is selected, are you sure you want to delete this VM? (Y/N): ")
                        if selection == "Y":
                            doublecheck=input("Please insert Full VM name here to confirm deletion: ")
                            if doublecheck == i.name:
                                print("Deletion in progress for ", i.name)
                                i.PowerOff()
                                sleep(10)
                                i.Destroy_Task()
                                print("VM has been successfully deleted")
                            else:
                                print("VM name does not match, deletion cancelled.")
                        elif selection == "N":
                            print("Not deleting ", i.name)
                            print()

            elif vmoption == 5:
                print("You Have Chosen to Reconfigure a VM's Resources")
                connect.si.RetrieveContent()
                datacenter = connect.si.content.rootFolder.childEntity[0]
                vms = datacenter.vmFolder.childEntity
                confvmname=input("Enter the name of the VM you want to reconfigure: ")
                for vm in vms:
                    if confvmname in str(vm.name):
                        selection=input(vm.name + " is selected, are you sure you want to reconfigure this VM? (Y/N): ")
                        if selection == "Y":
                            if vm.guest.guestState == "notRunning":
                                cpuchange=input("Do you  want to change the CPU count of " + vm.name + "? Current CPU Count is " + str(vm.config.hardware.numCPU) + " (Y/N):")
                                if cpuchange == "Y":
                                    CPUnum=input("How many CPUs do you want for this VM: ")
                                    Corenum=input("How many cores do you want on each CPU for this VM: ")
                                    cpuspec = vim.vm.ConfigSpec()
                                    cpuspec.numCPUs = int(CPUnum)
                                    cpuspec.numCoresPerSocket = int(Corenum)
                                    vm.Reconfigure(cpuspec)
                                    sleep(5)
                                    print(vm.name, "has been updated to have ", str(vm.config.hardware.numCPU), " CPUs.")
                                    print()
                                elif cpuchange == "N":
                                    print("No changes will be done to the CPU count of ", vm.name)
                                    print()
                                memchange=input("Do you  want to change the amount of memory on " + vm.name + "? Current amount of memory is " + str(vm.config.hardware.memoryMB/1024) + " GB (Y/N):")
                                if memchange == "Y":
                                    memnum=input("How much memory do you want for this VM (in GB): ")
                                    memnum = int(memnum)
                                    memnum = memnum*1024
                                    memspec = vim.vm.ConfigSpec()
                                    memspec.memoryMB = memnum
                                    vm.Reconfigure(memspec)      
                                    sleep(5)
                                    print(vm.name, "has been updated to have ", str(vm.config.hardware.memoryMB/1024), " GB of memory.")
                                    print()                              
                                elif memchange == "N":
                                    print("No changes will be done to the memory amount of ", vm.name)
                            else:
                                print(vm.name, " is currently powered on! You will need to power it down before reconfiguring.")
                                print()
                        elif selection == "N":
                            print()       
            elif vmoption == 6:
                print("W.I.P")

            else:
                print("Invalid option.")
            print()
            vmmenu()
            vmoption = int(input("Enter your option: "))
                        
    else:
        print("Invalid option.")

    print()
    menu()
    option = int(input("Enter your option: "))

Disconnect(connect.si)
print("Disconnecting, Goodbye.")