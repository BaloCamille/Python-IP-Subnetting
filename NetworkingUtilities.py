#the functions and classes in this file work with various networking objects, including:
    #Networks
    #IPs
    #Segments
    #Packets
    #Frames

#and functions:
    #processNetwork


#this function takes a string parameter that contains the IP, CIDR, and port in format:
    #X.X.X.X/X:X
#and processes it, returning the IP(string) and CIDR(string)/Port individually 
def processNetwork(toprocess):
    #this first decision structure will split and process an IP and /CIDR
    #evaluate if there is a "/" in the string
    if "/" in toprocess:
        #evaluate if there is also a ":" in the string
        if ":" in toprocess:
            #if so, split the string first by "/" (which would be the first character to split)
            processed = toprocess.split("/")
            #split the second value (at index 1) with the ":"
            #this is now a 2d list, with format: ["X.X.X.X", [X, X]]
            processed[1] = processed[1].split(":")
            #return the first value in the list at index 0
            #since the value at index 1 is another list, index further to split the list individually
            return processed[0], processed[1][0], processed[1][1]
        #if the strin only has "/" then split as such
        else:
            #split the string by "/"
            processed = toprocess.split("/")
            #return both values at the 2 indices
            return processed[0], processed[1]
    #this second decision structure will split and process an IP and :Port (socket address)
    #if there is only a ":" in the string, then split as such
    elif ":" in toprocess:
        #split the string by ":"
        processed = toprocess.split(":")
        #return both values at the 2 indices
        return processed[0], processed[1]
     
        
    

#the Network class is the superclass of the IP class
class Network:
    def __init__(self, netID, cidr, ip=""):
        #set the parameters for netID (network ID) and cidr (subnet mask length)
        #the netID parameter is a string with format: X.X.X.X
        self.netID = netID
        #the cidr parameter is an int
        self.cidr = int(cidr)
        #the ip paramter is a string set default to ""
        self.ip = ip

        #these attributes are initialized into all Network objects:
        #this list contains the 3 private networks
        self._privClasses = [["10.0.0.0", 8],["172.16.0.0", 16],["192.168.0.0", 16]]
        #this list represents the first quartet of class A networks
        self._netClassA = list(range(0,128))
        #this list represents the first quartet of class B networks
        self._netClassB = list(range(128,192))
        #this list represents the first quartet of class C networks
        self._netClassC = list(range(192,224))
        #this list represents the first quartet of class D networks
        self._netClassD = list(range(224,240))
        #this list represents the first quartet of class E networks
        self._netClassE = list(range(240,256))

        #call the toBinary method to convert to binary
        self._toBinary()

    #the following methods are all SET methods:

    #this method provides a way to set / change the netID of the Network 
    def setNetID(self, netID):
        self.netID = netID
    #this method provides a way to set / change the CIDR of the Network
    def setCIDR(self, cidr):
        self.cidr = cidr
    #this method adds an IP address to the Network
    def addIP(self, ip):
        #convert self.ip to a list to hold more than one ip address
        self.ip = list(self.ip)
        self.ip.append(ip)


    #the following methods are all processing methods:
    
    #this method converts: netID, CIDR, and broadcastID to binary
    #it is automatically called in the __init__ method and does not return anything
    #this method allows for other processes and subnetting to occur
    def _toBinary(self):
        #create the binary version of the subnet mask using the CIDR
        #for the value of the CIDR, print 1s in string form
        #for the value of 32 (the maximum subnet mask length) minus the cidr, print 0s
        #concatenate the 1s and 0s strings together to form the binary sunbet mask
        self._binSM = "1"*(self.cidr) + "0"*(32-self.cidr)

        #convert netID and broadcastID to binary
        if self.netID != "":
            #convert netID in format: X.X.X.X to 1s and 0s in a string
            #create a local variable to hold the temp binary string to later assign to self
            binNet = ""
            #split the 4 parts of the netID at "." and store the new list in a local variable
            #netparts will hold a string list that looks like: ["X","X","X","X"]
            netparts = self.netID.split(".")
            #create a for loop that converts each value in the list to its binary form
            for val in netparts:
                #convert val to an int and then into a binary sttring and store in binNum
                #splice off the first two 0b characters from the binary string
                binNum = bin(int(val))[2:]
                #pad with 0s to get to 8 "bits" long
                binNum = "0"*(8-len(binNum))+binNum
                #concatenate binNet with binNum
                binNet += binNum
            #set the local variable binNet to self 
            #this prevents logical errors from occuring if the method is called more than once
            self._binNetID = binNet
 
            #find the broadcast ID in binary
            #splice the netID at the length of the CIDR (int) to get the "bits" to turn "on"
            self._binBroad = self._binNetID[self.cidr:]
            #concatenate "1" as many as the length of the binary broadcast ID
            self._binBroad = "1"*len(self._binBroad)

            #append the network portion to the broadcast portion
            self._binBroad = self._binNetID[:self.cidr] + self._binBroad
        
        #convert ip to binary format
        if self.ip != "":
            #convert IP in format: X.X.X.X to 1s and 0s in a string
            #create a local variable to hold the temp binary string to later assign to self
            binIP = ""
            #split the 4 parts of the IP at "." and store the new list in a local variable
            #ipparts will hold a string list that looks like: ["X","X","X","X"]
            ipparts = self.ip.split(".")
            #create a for loop that converts each value in the list to its binary form
            for val in ipparts:
                #convert val to an int and then into a binary sttring and store in binNum
                #splice off the first two 0b characters from the binary string
                binNum = bin(int(val))[2:]
                #pad with 0s to get to 8 "bits" long
                binNum = "0"*(8-len(binNum))+binNum
                #concatenate binIP with binNum
                binIP += binNum
            #set the local variable binIP to self 
            #this prevents logical errors from occuring if the method is called more than once
            self._binIP = binIP


    
    #returns the netID
    def getNetID(self):
        return self.netID

    #this method finds the subnet mask from the CIDR 
    def getSubnetMask(self):
        #create an empty string to add to later to represent the numerical version of the subnet mask
        localSM = ""
        
        #use a for loop to splice and convert the binary strings to base 2 integers
        #start at i=8, end at i=33, step i+8 every iteraton
            #i will be used for splicing purposes
        for i in range(8, 33, 8):
            #qt is the quartet of the subnet mask, being comprised of 8 "bits"
            #splice from i-8 to i for each iteration
            #convert qt to an int with base 2
            qt = int(self._binSM[i-8:i], 2)
            #convert qt to a string and concatenate it to the subnet mask string with a "."
            localSM += str(qt) + "."
        #strip the last period from the end of the subnet mask
        localSM = localSM.rstrip(".")

        #set the localSM to self
        self.SM = localSM

        #return the subnet mask as a string but in numerical form
        return self.SM
    #this method finds the broadcast ID from the netID and the SM (in numeric/strng form not binary)
    def getBroadcastID(self):
        #create a local variable for the broadcast ID
        localBroad = ""
        #use a for loop to splice and convert the binary strings to base 2 integers
        #start at i=8, end at i=33, step i+8 every iteraton
            #i will be used for splicing purposes
        for i in range(8, 33, 8):
            #qt is the quartet of the broadcast, being comprised of 8 "bits"
            #splice from i-8 to i for each iteration
            #convert qt to an int with base 2
            qt = int(self._binBroad[i-8:i], 2)
            #convert qt to a string and concatenate it to the subnet mask string with a "."
            localBroad += str(qt) + "."
        #strip the last period from the end of the subnet mask
        localBroad = localBroad.rstrip(".")
        
        #set the local variable to self
        self.broadID = localBroad

        #return the broadcast ID in numerical form
        return self.broadID
    #return the CIDR
    def getCIDR(self):
        return self.cidr
    
    #this method finds the total hosts possible in the Network
    def getTotalHosts(self):
        #2 to the power of (32-cidr) will equal all possible hosts
            #this is a general networking equation to find hosts
        self.totalHostsNum = 2**(32-self.cidr)
        #return the value
        return self.totalHostsNum

    #this method finds the usable hosts posisble in the Network
    def getUsableHosts(self):
        #2 to the power of (32-cidr) -2 will equal all usable hosts
            #subtract 2 because the netID and broadcastID are not usable
            #this is a general networking equation to find hosts
        self.usableHostsNum = 2**(32-self.cidr)-2
        #return the value
        return self.usableHostsNum
    
    #this method finds the range of IPs in the Network
    def getNetworkRange(self):
        #call this method to make sure that the broadcastID was converted to a numeric (non binary) form
        #if it is not called in the main program before this method is called, an error will occur
        #because self.broadID has an empty value
        #by calling it regardless, it ensures that self.broadID has a value
        self.getBroadcastID()
        #create local variables to hold a list of the 4 parts of the network ID and broadcast ID
        #index the value at 3 (the fourth/last value) which is the last quartet in the address
        #convert to int
        netparts = int(self.netID.split(".")[3])
        broadparts = int(self.broadID.split(".")[3])

        #add 1 to the network ID (netparts)
        netparts += 1
        #subtract 1 from the broadcast ID (broadparts)
        broadparts -= 1

        #create local variables to hold the split values of the netID and broadcastID in a list
        listFirst = self.netID.split(".")[:3]
        listLast = self.broadID.split(".")[:3]

        #create two local variable to use later to hold the string value of the IPs
        localFirst = ""
        localLast = ""

        #use a for loop to iterate over the 3 values held in the lists created earlier
        for val in listFirst:
            #concatenate the local string variable with the val in the list and a "."
            localFirst += val + "."
        #convert netparts (int) to string
        #concatenate netparts to localFirst to find the first usbale IP
        localFirst += str(netparts)
        
        #use a for loop to iterate over the 3 values held in the lists created earlier
        for val in listLast:
            #concatenate the local string variable with the val in the list and a "."
            localLast += val + "."
        #convert broadparts (int) to string
        #concatenate broadparts to localLast to find the last usbale IP
        localLast += str(broadparts)

        #create a list that holds both values of the first usbale IP and the last usable IP
        self.netRange = [localFirst, localLast]
        
        #return the list with the first usbale IP and the last usbale IP in the format of a list
        return self.netRange
    
    #this method determines the network class of the Network and whether it is a private net or not
    def getNetworkClass(self):
        #create a local variable that will hold the netID (string) and CIDR (int)
        localClass = [self.netID, self.cidr]

        #evaluate if the localClass list is found in the _private network class list
        if localClass in self._privClasses:
            #if it is in the _privClasses list, set self.private to PRIV
            self.private = "Private IP Class"
        #if not found in _privClasses list
        else:
            #if not found, set self.private to NOT
            self.private = "Not a Private IP Class"
        
        #create a local variable to hold a list of the netID parts (4 parts)
        #split by "."
        netparts = self.netID.split(".")
        #reassign netparts to the first index which is the first quartet
        #convert from string to int
        netparts = int(netparts[0])

        #evaluate the class the network is in
        if netparts in self._netClassA and self.cidr == 8:
            self.netClass = "A"
        elif netparts in self._netClassB and self.cidr == 16:
            self.netClass = "B"
        elif netparts in self._netClassC and self.cidr == 24:
            self.netClass = "C"
        elif netparts in self._netClassD:
            self.netClass = "D"
        elif netparts in self._netClassE:
            self.netClass = "E"
        else:
            self.netClass = "other"
        #return the class and whether it is private or not in a list format
        return [self.netClass, self.private]
           
    
    
    #the following methods are all GET methods:

    #this method provides a way to get the list of IPs added to the Network
    def getIPs(self):
        return self.ip

        
    



#the IP class is a subclass of the Network class and inherits / extends the Network class
class IP(Network):
    def __init__(self, ip, cidr, port, netid=""):
        super().__init__(netid, cidr, ip)
        self.port = int(port)
        self._portProtocols = {
            20:["File Transfer Protocol-Data","TCP"], 
            21:["File Transfer Protocol-Control","TCP"], 
            22:["Secure Shell","TCP"], 
            23:["Telnet","TCP"], 
            25:["Simple Mail Transfer Protocol","TCP"], 
            53:["Domain Name Servces","TCP/UDP"], 
            67:["Dynamic Host Configuration Protocol-Server", "UDP"],
            68:["Dynamic Host Configuration Protocol-Client","UDP"], 
            69:["Trivial File Transfer Protocol", "UDP"], 
            80:["Hypertext Transfer Protocol", "TCP"], 
            110:["Post Office Protocol 3", "TCP"], 
            143:["Internet Message Access Protocol", "TCP"],
            161:["Simple Network Management Protocol","UDP"], 
            443:["Hypertext Transfer Protocol Secure", "TCP"],
            7:["Echo", "TCP/UDP"], 
            123:["Network Time Protocol","UDP"], 
            156:["SQL","TCP/UDP"], 
            179:["Border Gateway Protocol", "TCP"],
            389:["LDAP", "TCP"], 
            520:["Routing Information Protocol", "UDP"], 
            636:["LDAPS","TCP"], 853:["DNS over TLS","TCP"],
            993:["Internet Message Access Protocol Secure","TCP"], 
            992:["Telnet over TLS/SSL","TCP/UDP"], 
            995:["Post Office Protocol 3 Secure", "TCP/UDP"]
            }
        
        #call the subnet method automatically to subnet the ip and cidr
        self._Subnet()

        #call the getNetID method to initialize the networkID
        self.getNetID()
    
    #the following methods are SET methods:

    #this method provides a way to set / change the ip of the IP
    def setIP(self, ip):
        self.ip = ip
    #this method provides a way to set / change the CIDR of the IP
    def setCIDR(self, cidr):
        self.cidr = cidr
    #this method provides a way to set / change the port of the IP
    def setPort(self, port):
        self.port = port
    
    #the following methods are all processing methods:

    #this method subnets an ip and its CIDR to determine its netID and broadcastID
    def _Subnet(self):
        #create a local variable to hold the netID and initialize it to an empty string to later use
        localNetID = ""

        #use a for loop to iterate through the binary IP and SM
        for i, ipBit in enumerate(self._binIP):
            #set the subnet mask bit to the self variable stroing the binary string
            #index the self binary string at the same iteration as the ipBit
            smBit = self._binSM[i]
            #perform the ANDing process to evaluate each bit at a time in both the IP and SM
            #if both the bit in IP and the SM are 1, concatenate a 1 to the local variable netID
            if ipBit == "1" and smBit == "1":
                localNetID += "1"
            #else, if they are both not one, concatenate a 0 to the local variable netID
            else:
                localNetID += "0"
        #set the local variable to equal the self variable
        self._binNetID = localNetID


        #find the broadcast ID
        #create a local variable to hold the splice of the netID
        #set the local variable sm to equal the splice of everything to the left of the cidr length
        #this will be the amount of "bits" to "turn on"
        sm = self._binNetID[self.cidr:]

        #pad the local variable with 1s so that it is equal to the length of the cidr (subnet mask)
        sm = "1"*len(sm)

        #append the network portion to the subnet mask portion to get the broadcast it
        self._binBroad = self._binNetID[:self.cidr] + sm
    #this method gives the network id in the numerical (string) form
    def getNetID(self):
        #create a local variable for the network ID
        localNet = ""
        #use a for loop to splice and convert the binary strings to base 2 integers
        #start at i=8, end at i=33, step i+8 every iteraton
            #i will be used for splicing purposes
        for i in range(8, 33, 8):
            #qt is the quartet of the network ID, being comprised of 8 "bits"
            #splice from i-8 to i for each iteration
            #convert qt to an int with base 2
            qt = int(self._binNetID[i-8:i], 2)
            #convert qt to a string and concatenate it to the subnet mask string with a "."
            localNet += str(qt) + "."
        #strip the last period from the end of the subnet mask
        localNet = localNet.rstrip(".")
        
        #set the local variable to self
        self.netID = localNet

        #return the netid in numerical string form
        return self.netID
    #this method returns the port of the IP
    def getPort(self):
        return self.port
    #return the ip
    def getIP(self):
        return self.ip
    #this method evaluates the port the IP is being used with and the port's corresponding protocol
    def getProtocol(self):
        #evaluate if the port is in the port protocol dictionary
        if self.port in self._portProtocols:
            #if so, set the protocol to be the value at the port (which is the key)
            self.protocol = self._portProtocols[self.port]
            #return the protocol being used with that particular port number
            return self.protocol
        #evaluate if the port is within the range of the designated well known port numbers
        elif self.port > 0 and self.port <= 1023:
            #if it isn't a common port (a port found in the protocol dictionary), set protocol to 
            #the type of port is usually assigned to it
            self.protocol = "Well-Known Protocol"
            #return the type of port / protocol that is usually assinged to that range
            return self.protocol
        #evaluate if the port is within the range of the designated registered port numbers
        elif self.port >= 1024 and self.port <= 49151:
            #set the protocl to Registered Port
            self.protocol = "Registered Protocol"
            #return the protocol
            return self.protocol
        #evaluate if the port is within the range of the dynamic port numbers
        elif self.port >= 49152 and self.port <= 65535:
            #assign protocol to Dynamic Port
            self.protocol = "Dynamic Protocol"
            #returm the protocol
            return self.protocol
        #if none of this is true, set the port to unknown
        else:
            #set the protocol to unknown
            self.protocol = "Unknown Protocol"
            #return the protocol
            return self.protocol
        


