#Alex Shapovalov
#CS 5220
#Programming Assignment #4, Branch Prediction

def main():
    #create branch dictionary (array was not a good idea)
    branches = {}

    filename = "curl1m.btrace.txt"

    with open(filename, 'r') as file:
        for line in file:
            instruction = line.split()

            address = instruction[0]

            value = int(instruction[1])

            # if branch is new, add to dictionary
            if address not in branches:
                branches[address] = {"taken": 0, "skipped": 0, "total": 0}

            # add tallies based on branch taken / not taken
            if value == 0:
                branches[address]["skipped"] += 1
                branches[address]["total"] = branches[address]["skipped"] + branches[address]["taken"]
            else:
                branches[address]["taken"] += 1
                branches[address]["total"] = branches[address]["skipped"] + branches[address]["taken"]

    for address, i in branches.items():
        print("address: " + str(address) + ", taken: " + str(i['taken']) + ", skipped: " + str(i['skipped']) + ", total: " + str(i['total']))

    #do calculations in the array

main()