#Python final project written by Camille Balo

#import the Networkingutilities file 
import NetworkingUtilities as net

#create global constants to represent the different menu options
RAW = 1
SUMMARY = 2
NETWORK = 3
PORT = 4
EXIT = 5


def main():
    #initialize the option variable to -1
    option = -1

    #load the data 
    input("Press any key to load the data. ")
    totalIPs, totalNets, netIDs = loadData()

    #use a while loop to go back and forth between menu options
    while option != EXIT: 
        #call the printMenu method
        option = printMenu()

        #use a decision structure to process the option 
        if option == RAW:
            getRawData()
        elif option == SUMMARY:
            getSummary(netIDs, totalIPs)
        elif option == NETWORK:
            getNetworkData(totalNets)
        elif option == PORT:
            getPortData(totalIPs)


#the printMenu function will:
    # print the menu options
    # get user input
    # validate user input
    # return user input
def printMenu():
    #print the main menu options
    print()
    print("\t\tNetwork Analysis")
    print("----------------------------")
    print("1. View Raw Data")
    print("2. View Summary")
    print("3. View Network Data")
    print("4. View Port Data")
    print("5. Exit")
    print()

    #get user input
    choice = int(input("Enter an option: "))

    #validate the input
    while choice < RAW or choice > EXIT:
        choice = int(input("Invalid input. Enter an option: "))

    #return the input
    return choice

#the loadData function will:
    # read-in each line from the .txt file
    # initially process the data
    # return a list of IPs (objects), Networks (objects), and NetIDs (strings)
def loadData():
    #create an ip list and a network list to hold all of the ips and networks (objects)
    totalIPs = []
    totalNets = []
    #create a list to hold the netIDs of each of the network objects
    #this list will only hold the unique network ids
    netIDs = []

    #use a try / except statement to open the SocketsAddress.txt file 
    try:
        #open the .txt file with read abilities
        ipFile = open("SocketsAddress.txt", 'r')
    #if the file cannot be found and an execption is raised for that reason, print file not found
    except FileNotFoundError:
        print("The file could not be found.")
    #if any other exception is raised while trying to open the file, print an error has occurred
    except Exception:
        print("An error has occurred.")


    #read-in each line of the file using a for loop
    for line in ipFile:
        #strip the /n (newline character) from the line
        readIP = line.rstrip("\n")

        #call the processNetwork function from the util file to split the line
        #processNetwork returns 2-3 values (depending on what is in the string that is passed)
        #since we know the structure of the file and that there are 3 parts to each line
        #(ip, cidr, and port), 3 varibles will be set equal to the processNetwork function
        ip, cidr, port = net.processNetwork(readIP)

        #create an IP object for each ip read-in
        #pass in the ip, cidr, and port returned from the processNetwork function
        ipObj = net.IP(ip, cidr, port)

        #append the ipObj to the totalIPs list
        totalIPs.append(ipObj)
    
    #close the file
    ipFile.close()


    #use a for loop to iterate through all of the ipObj's network IDs
    #begin by iterating over all the ip objects held in the totalIPs list
    for obj in totalIPs:
        #set the ipNet variable to equal the ip object's network ID
        ipNet = obj.getNetID()

        #if the network ID is already in the netIDs list, add the IP to the corresponding network obj
        if ipNet in netIDs:
            #iterate over all of the network objects in the network object list
            for netobj in totalNets:
                #if the ip netID is equal to the network object's netID, add that IP to the network
                if ipNet == netobj.getNetID():
                    #add the IP to the corresponding network
                    netobj.addIP(obj.getIP())

        #if the ip object's netID is not in the netIDs list, add it
        if ipNet not in netIDs:
            #create a new network object with that netID and cidr
            netObj = net.Network(obj.getNetID(), obj.getCIDR())
            #append the network to the network list (for the network objects)
            totalNets.append(netObj)
            #add that ip object's ip to that network
            netObj.addIP(obj.getIP())
            #append the netID of that network object to the netIDs list
            netIDs.append(netObj.getNetID())


    #confirm the data was loaded
    input("The data was loaded successfully. ")

    #return the totalIPs list to later be used for other functions
    return totalIPs, totalNets, netIDs

#the getRawData function will:
    # read-in ech line from the .txt file
    # print each line in the .txt file
def getRawData():
    #use a try / except statement to open the SocketsAddress.txt file 
    try:
        #open the .txt file with read abilities
        ipFile = open("SocketsAddress.txt", 'r')
    #if the file cannot be found and an execption is raised for that reason, print file not found
    except FileNotFoundError:
        print("The file could not be found.")
    #if any other exception is raised while trying to open the file, print an error has occurred
    except Exception:
        print("An error has occurred.")
    
    #read in each line of the file and print the raw data
    for line in ipFile:
        #strip the newline character from the line
        readLine = line.rstrip("\n")

        #print the stripped line
        print(readLine)
        
    #confirm the raw data has finished printing
    input("All raw data has been displayed. ")

#the getSummary function will:
    # require a list of network objects and a list IP objects
    # print the amount of unique networks and IPs in the .txt file
def getSummary(net, IP):
    print()
    print("Summary")
    print(f"\tThere are {len(net)} unique networks")
    print(f"\tThere are {len(IP)} IP addresses")
    print()
    input("The summary has been displayed. ")

#the getNetworkData function will:
    # require a list of network objects
    # determine the:
        # most common network (and its associated data)
        # private networks (and its asociated data)
        # the Class A-E networks present
    # print the network data
def getNetworkData(totalNets):
    #find the most common Network ID (the network object with the most IPs assigned to it)
    #create a variable to hold the object that has the most IPs assigned to it
    #initialize the variable with the first value of the totalNets list to compare to the other objs
    commonNet = totalNets[0]

    #iterate through all of the network objects in the totalNets list
    for netobj in totalNets:
        numIPs = len(netobj.getIPs())
        if numIPs > len(commonNet.getIPs()):
            commonNet = netobj
    
    #get all the private networks
    #create a list that will store the private networks 
    privateNets = []
    #iterate through all of the network objects in totalNets
    for netobj in totalNets:
        #call the getNetworkClass method to initialize the network's ip class and private status
        netobj.getNetworkClass()
        #if the network object's private attribute is private, append to the private list
        if netobj.private == "Private IP Class":
            #append the network object' netID to the privateNets list
            privateNets.append(netobj.getNetID())

    #get all the class A networks
    #create a list that will store the class A networks
    classAnets = []
    #iterate through all of the network objects in totalNets
    for netobj in totalNets:
        #if the netobj's class is A, append it to the classAnets list
        if netobj.getNetworkClass()[0] == "A":
            #append the netID of the netobj to the list
            classAnets.append(netobj.getNetID())
    
    #get all the class B networks
    #create a list that will store the class B networks
    classBnets = []
    #iterate through all of the network objects in totalNets
    for netobj in totalNets:
        #if the netobj's class is B, append it to the classBnets list
        if netobj.getNetworkClass()[0] == "B":
            #append the netID of the netobj to the list
            classBnets.append(netobj.getNetID())
        
    
    #get all the class C networks
    #create a list that will store the class C networks
    classCnets = []
    #iterate through all of the network objects in totalNets
    for netobj in totalNets:
        #if the netobj's class is C, append it to the classCnets list
        if netobj.getNetworkClass()[0] == "C":
            #append the netID of the netobj to the list
            classCnets.append(netobj.getNetID())

    #get all the class D networks
    #create a list that will store the class D networks
    classDnets = []
    #iterate through all of the network objects in totalNets
    for netobj in totalNets:
        #if the netobj's class is D, append it to the classDnets list
        if netobj.getNetworkClass()[0] == "D":
            #append the netID of the netobj to the list
            classDnets.append(netobj.getNetID())
    
    #get all the class E networks
    #create a list that will store the class E networks
    classEnets = []
    #iterate through all of the network objects in totalNets
    for netobj in totalNets:
        #if the netobj's class is E, append it to the classEnets list
        if netobj.getNetworkClass()[0] == "E":
            #append the netID of the netobj to the list
            classEnets.append(netobj.getNetID())




    print()
    print("\nNetwork Data")
    print(f"\tThe most common network ID is: {commonNet.getNetID()} with CIDR: /{commonNet.getCIDR()}")
    print(f"\t\t{commonNet.getNetID()} has {commonNet.getTotalHosts():,} total hosts")
    print(f"\t\t{commonNet.getNetID()} has {commonNet.getUsableHosts():,} usable hosts")
    print(f"\t\tThe network range of {commonNet.getNetID()} is: {commonNet.getNetworkRange()[0]} - {commonNet.getNetworkRange()[1]} ")
    print(f"\t\t{commonNet.getNetID()} is a Class {commonNet.getNetworkClass()[0]} network")
    print(f"\t\t{commonNet.getNetID()} is {commonNet.getNetworkClass()[1]}")
    print(f"\t\t{commonNet.getNetID()} has the following IPs currently assigned to it:")
    #iterate through the list of IPs in the most common network and print out the ip
    for val in commonNet.getIPs():
        print(f"\t\t\t{val}")

    print(f"\n\tThere are {len(privateNets)} private networks currently in use, including:")
    #iterate through the values in the privateNets list to print them out
    for val in privateNets:
        print(f"\t\t{val}")


    print(f"\tThere are {len(classAnets)} Class A networks currently in use")
    print(f"\tThere are {len(classBnets)} Class B networks currently in use")
    print(f"\tThere are {len(classCnets)} Class C networks currently in use")
    print(f"\tThere are {len(classDnets)} Class D networks currently in use")
    print(f"\tThere are {len(classEnets)} Class E networks currently in use")
    print()
    input("The Network Data has been displayed. ")

#the getPortData function will:
    # require a list of IP objects
    # determine the:
        # lowest / highest port number being used
        # common protocols
        # known/registerd/dynamic ports
    #print the port data
def getPortData(totalIPs):
    #get the lowest port number being used
    #create a list to hold all of the ports being used with each IP
    totalPorts = []
    #iterate through all of the ip objects in the totalIPs list
    for ipobj in totalIPs:
        totalPorts.append(ipobj.getPort())
    #create a variable to hold the lowest port number and initialize to the first ip obj in the list
    lowestPort = totalIPs[0]
    #iterate through all of the ip objects in the totalIPs list
    for ipobj in totalIPs:
        #create a varaible to hold the current ip object's port
        ipport = ipobj.getPort()
        #if the ip obj's port is less than the ip object's port number stored in the lowestPort variable
        if ipport < lowestPort.getPort():
            #set lowestPort to be the object that has a lower port number
            lowestPort = ipobj
    
    #get the highest port number being used
    #create a variable to hold the highest port number and initialize to the first ip obj in the list
    highestPort = totalIPs[0]
    #iterate through all of the ip objects in the totalIPs list
    for ipobj in totalIPs:
        #create a varaible to hold the current ip object's port
        ipport = ipobj.getPort()
        #if the ip obj's port is greater than the ip object's port number stored in the highestPort variable
        if ipport > highestPort.getPort():
            #set lowestPort to be the object that has a lower port number
            highestPort = ipobj
    
    #get all the common protocols being used
    #create a list to hold all of the ip objects using common port numbers
    commonPorts = []
    #iterate through all of the ip objects in the totalIPs list
    for ipobj in totalIPs:
        #if the ipobj's port is in the common ports dictionary, append the object to the list
        if ipobj.port in ipobj._portProtocols:
            #append the ip obj to the commonPorts list
            commonPorts.append(ipobj)
    
    #create a new list to hold the actual protocol/port being used rather than just the obj
    #this list will hold all the unique values of protocols (no duplicates)
    commonProtocols = []
    #iterate through the ip objects with common protocols held in the commonPorts list
    for obj in commonPorts:
        if obj.getProtocol()[0] not in commonProtocols:
            commonProtocols.append(obj.getProtocol()[0])
    
    #get the number of well-known ports being used
    #create a variable to hold the number of well known ports being used by the ip objs
    #initialize the knownPorts counter variable to 0
    knownPorts = 0

    #iterate through all the ip objects in the totalIPs list
    for ipobj in totalIPs:
        #if the protocol of the current ip object is a well known protocol, increment by 1
        if ipobj.getProtocol() == "Well-Known Protocol":
            #increment the knownPorts counter variable by 1
            knownPorts += 1
    
    #get the number of registered ports being used
    #create a variable to hold the number of registered ports being used by the ip objs
    #initialize the regPorts counter variable to 0
    regPorts = 0

    #iterate through all the ip objects in the totalIPs list
    for ipobj in totalIPs:
        #if the protocol of the current ip object is a registered protocol, increment by 1
        if ipobj.getProtocol() == "Registered Protocol":
            #increment the regPorts counter variable by 1
            regPorts += 1

    #get the number of dynamic ports being used
    #create a variable to hold the number of dynamic ports being used by the ip objs
    #initialize the dynPorts counter variable to 0
    dynPorts = 0

    #iterate through all the ip objects in the totalIPs list
    for ipobj in totalIPs:
        #if the protocol of the current ip object is a dynamic protocol, increment by 1
        if ipobj.getProtocol() == "Dynamic Protocol":
            #increment the dynPorts counter variable by 1
            dynPorts += 1

    #display the data
    print()
    print("\nPort Data")
    print(f"\tThe lowest port number used is: {lowestPort.getPort()}")
    print(f"\t\tThe IP that is using this port is: {lowestPort.getIP()}")

    print(f"\tThe highest port number used is: {highestPort.getPort()}")
    print(f"\t\tThe IP that is using this port is: {highestPort.getIP()}")

    print(f"\tThe amount of common protocols being used is {len(commonPorts)}, including:")
    #iterate through the values in the commonPorts list
    for val in commonProtocols:
        #print the protocols
        print(f"\t\t{val}")

    print(f"\tThere are {knownPorts} Well-Known Ports being used")
    print(f"\tThere are {regPorts} Registered Ports being used")
    print(f"\tThere are {dynPorts} Dynamic Ports being used")
    print()

    input("The port data has been displayed. ")




if __name__ == '__main__':
    main()