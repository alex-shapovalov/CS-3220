#Alex Shapovalov
#CS 5220
#Programming Assignment #4, Branch Prediction

class Branch:
    def __init__(self, address):
        self.address = address
        self.numTaken = 0
        self.numSkipped = 0
        self.total = self.numTaken + self.numSkipped

def main():
    branches = {}

    filename = "curl1m.btrace.txt"

    with open(filename, 'r') as file:
        for line in file:
            instruction = line.split()
            address = instruction[0]
            value = int(instruction[1])  # Convert value to integer (0 or 1)

            # Check if address exists in dictionary
            if address not in branches:
                branches[address] = {"taken": 0, "skipped": 0}  # Initialize with counts

            # Update counts based on value
            if value == 0:
                branches[address]["skipped"] += 1
            else:
                branches[address]["taken"] += 1

    # Calculate totals (optional)
    for address, counts in branches.items():
        counts["total"] = counts["taken"] + counts["skipped"]

    # Print results
    for address, counts in branches.items():
        print(f"Address: {address}, Taken: {counts['taken']}, Skipped: {counts['skipped']}")

    #if branch is new, add to array branches

    #else add another tally to that branch in the array


    #do calculations in the array

main()