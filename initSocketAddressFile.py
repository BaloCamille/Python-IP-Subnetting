#import random to generate random numbers to create the ips, cidrs, and sockets
import random as r

#open the SocketsAddress.txt file with write ability
#the reason it is with write ability rather than append ("a") ability is because this prevents
#the file from becoming too large if you run this particular file more than once and it allows
#you to test the main program better since the values can be changed easier

#try opening the file with a TRY EXCEPT statement to gracefully handle any exceptions that may raise
try:
    filename = open("SocketsAddress.txt", "w")
#except the specific exception of the file not being found
except FileNotFoundError:
    #print that the file was not found
    print("File not found.")
#catch all exceptions that may occur
except Exception:
    #print that an error has occured
    print("An error has occured.")

#generate random numbers to use to later generate random addresses to write to the file
ran1 = r.randint(150, 250)
ran2 = r.randint(250, 350)
ran3 = r.randint(350, 550)
ran4 = r.randint(10, 75)



#use a for loop to generate 200 ips with all possible sockets (ports) values
#class A network address generation
for i in range(ran1):
    #one is the value of the first quartet of the ip
    one = r.randint(1,127)
    #two is the value of the second quartet of the ip
    two = r.randint(1,255)
    #three is the value of the third quartet of the ip
    three = r.randint(1,255)
    #four is the value of the fourth quartet of the ip
    four = r.randint(1,255)
    #the cidr is the length of the subnet mask, from 8 to 12 (for class A)
    cidr = r.randint(8,12)
    #the socket is the port the ip is being used with 
    #these are all possible ports
    socket = r.randint(1,65535)
    #structure the address in the designated format
    addr = f"{one}.{two}.{three}.{four}/{cidr}:{socket}"
    #write it to the file with a newline character
    filename.write(addr + "\n")

#repeat the same process as above but with different socket ranges
#class B
for i in range(ran2):
    one = r.randint(128,191)
    two = r.randint(1,255)
    three = r.randint(1,255)
    four = r.randint(1,255)
    cidr = r.randint(15, 23) 
    socket = r.randint(1,1000)
    addr = f"{one}.{two}.{three}.{four}/{cidr}:{socket}"
    filename.write(addr + "\n")
 
#repeat the same process as above but again, with different socket ranges
#class C
for i in range(ran3):
    one = r.randint(192,223)
    two = r.randint(1,255)
    three = r.randint(1,255)
    four = r.randint(1,255)
    cidr = r.randint(24,30)
    socket = r.randint(1,500)
    addr = f"{one}.{two}.{three}.{four}/{cidr}:{socket}"
    filename.write(addr + "\n")

#repeat the same process as above but again, with different socket ranges
#class D/E
for i in range(ran1):
    one = r.randint(224,255)
    two = r.randint(1,255)
    three = r.randint(1,255)
    four = r.randint(1,255)
    cidr = r.randint(8, 30)
    socket = r.randint(1,500)
    addr = f"{one}.{two}.{three}.{four}/{cidr}:{socket}"
    filename.write(addr + "\n")


#repeat process but for private IP spaces
for i in range(ran4):
    one = r.choice([10, 172, 192])
    two = r.choice([16, 168])
    three = r.randint(1,255)
    four = r.randint(1,255)
    cidr = r.choice([8,16])
    socket = r.randint(1,200)
    addr = f"{one}.{two}.{three}.{four}/{cidr}:{socket}"
    filename.write(addr + "\n")

#close the file
filename.close()