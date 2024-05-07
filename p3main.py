"""
COMPSCI 424 Program 3
Name: Jake Menning
"""


"""

I was unable to finish Program 3 due to me focusing on other projects/labs from other courses.
I still belive I will come out of the class with an alright grade, and I would like to prioritize my more at-risk courses.

"""



import os
import sys
import threading  # standard Python threading library

# (Comments are just suggestions. Feel free to modify or delete them.)

# When you start a thread with a call to "threading.Thread", you will
# need to pass in the name of the function whose code should run in
# that thread.

# If you want your variables and data structures for the banker's
# algorithm to have global scope, declare them here. This may make
# the rest of your program easier to write. 
#  
# Most software engineers say global variables are a Bad Idea (and 
# they're usually correct!), but systems programmers do it all the
# time, so I'm allowing it here.
#global num_resources
#global num_processes


# Let's write a main method at the top
def main():
    # Code to test command-line argument processing.
    # You can keep, modify, or remove this. It's not required.
    if len(sys.argv) < 3:
        sys.stderr.write("Not enough command-line arguments provided, exiting.")
        sys.exit(1)

    print("Selected mode:", sys.argv[1])
    print("Setup file location:", sys.argv[2])

    # 1. Open the setup file using the path in argv[2]
    global num_resources
    global num_processes
    with open(sys.argv[2], 'r') as setup_file:
        # 2. Get the number of resources and processes from the setup
        # file, and use this info to create the Banker's Algorithm
        # data structures
        
        num_resources = int(setup_file.readline().split()[0])
        print(num_resources, "resources")
        num_processes = int(setup_file.readline().split()[0])
        print(num_processes, "processes")

        print("\n")
        print(setup_file.readline().rstrip("\n")) # reads the "Available" string; strips the newLine character at the end
        global available
        available = []
        availablechar = setup_file.readline().split()
        #print(availablechar)
        for i in availablechar: # inputs the read characters into a integer list
            available.append(int(i))
        print(available)

        print("\n")
        print(setup_file.readline().rstrip("\n")) # reads the "Max" string; strips the newLine character at the end
        global max
        max = []
        maxchar = []
        for i in range(0, num_processes):
            maxchar.append(setup_file.readline().split())
        #print(maxchar)
        for i in range(0, num_processes):
            max.append([])
            for j in range(0, num_resources):
                max[i].append(int(maxchar[i][j])) # inputs the read characters into a 2d integer list
        print(max)
        
        print("\n")
        print(setup_file.readline().rstrip("\n")) # reads the "Allocation" string; strips the newLine character at the end
        global allocation
        allocation = []
        allocationchar = []
        for i in range(0, num_processes):
            allocationchar.append(setup_file.readline().split())
        #print(allocationchar)
        for i in range(0, num_processes):
            allocation.append([])
            for j in range(0, num_resources):
                allocation[i].append(int(allocationchar[i][j])) # inputs the read characters into a 2d integer list
        print(allocation)
            
        
        print("\nNeed") # otherwise known as potential requests
        global need
        need = []
        for i in range(0, num_processes):
            need.append([])
            for j in range(0, num_resources):
                need[i].append(max[i][j] - allocation[i][j]) # calculates need 2d array based on max - allocation
        print(need)
        
        print("\nWork") # otherwise known as the new available
        global work
        work = []
        for j in range(0, num_resources):
            work.append(available[j]) # copy of available
        print(work)

        print("\nFinish") # used for checking safe state
        global finish
        finish = []
        for i in range(0, num_processes):
            finish.append(False) # inputting False into each finish process status
        print(finish)

        print("\nTotal Allocation") # I made this variable because I found it difficult doing the math for the sumation of i sigma symbol for Allocation
        global totalAllocation
        totalAllocation = []
        for j in range(0, num_resources):
            sum = 0
            for i in range(0, num_processes):
                sum = sum + allocation[i][j] # calculates sum of allocations for each resource
            totalAllocation.append(sum)
        print(totalAllocation)

        print("\nTotal")
        global total
        total = []
        for j in range(0, num_resources):
            total.append(totalAllocation[j]+available[j])
        print(total)


        # 3. Use the rest of the setup file to initialize the data structures
        # (you fill in this part)
    
    # 4. Check initial conditions to ensure that the system is
    # beginning in a safe state: see "Check initial conditions"
    # in the Program 3 instructions
    terminate = False

    # check number 1
    for i in range(0, num_processes):
        for j in range(0, num_resources):
            if((False == (allocation[i][j] <= max[i][j]))): # check number 1
                print("Your Allocation[",i,"][",j,"] is not less than or equal to Maximum[",i,"][",j,"]")
                terminate = True
    
    # check number 2 which should always be True and not go into the if statement anyways.
    for j in range(0, num_resources):
        if((False == (total[j] == totalAllocation[j] + available[j]))): # check number 2 which should always be True and not go into the if statement anyways.
            print("You should never get here. Your Total resources somehow do not match the sum of your Available and Allocated resources.")
            terminate = True

    # check number 3; the system is in a safe state. Checking if claim graph is completely reducible.
    passed = safeState()
    if (False == passed):
        print("Safe State was not completed. A complete claim graph reduction could not be performed.")
        terminate = True

    if(terminate == True):
        return -1
    


    # 5. Go into either manual or automatic mode, depending on
    # the value of args[0]; you could implement these two modes
    # as separate methods within this class, as separate classes
    # with their own main methods, or as additional code within
    # this main method.
    arg1 = sys.argv[1]
    arg1 = arg1.lower()
    if(arg1 == "manual"):
        manual()
    elif(arg1 == "auto"):
        auto()
    # END OF MAIN

# fill in other methods here as desired
def safeState():
    while(finish.count(False) >= 1):
        for i in range(0, num_processes):
            passed = True
            for j in range(0, num_resources):
                if(finish[i] == True or need[i][j] > work[j]):
                    passed = False
            if(passed == True):
                finish[i] = True
                for j in range(0, num_resources):
                    work[j] = work[j] + allocation[i][j]
            print("need: ", i,"  ", need[i])
            print("allocation: ", i, "  ", allocation[i])
            print("Work: ", work)
            print("finish: ", finish)
    passed = True
    for i in range(0, num_processes):
        if(finish[i] == False):
            passed = False
    if(passed == True):
        return True
    elif(passed == False):
        return False

def manual():
    var = "test"
    while(var != "end"): 
        magic(var) # function to figure it out
        var = input("Enter commands into the terminal in the following order (replace the UNITS, RESOURCE, and PROCESS with integers for the elements being requested, the resource type ID being requested, and the process ID making the request): 'request UNITS of RESOURCE for PROCESS', 'release UNITS of RESOURCE for PROCESS', and 'end'.\n\nEnter your commands below: ")
        var = var.lower()

def auto():
    var =1

def bankers():
    var =1

def magic(str):
    command = []
    command = str.split()
    if(command[0] != "request" and command[0] != "release"):
        return 0 # return to manual because they didn't enter "request" or "release"
    if(command[2] != "of"):
        return 0 # return to manual because they didn't enter "of"
    if(command[4] != "for"):
        return 0 # return to manual because they didn't enter "for"
    
    rtn = [] 
    rtn.append(int(command[1])) # utils
    rtn.append(int(command[3])) # resource
    rtn.append(int(command[5])) # process

    #if(command[0] == "request" and rtn[0] )



    print(command)
    print(rtn)

    bankers()


main() # call the main function