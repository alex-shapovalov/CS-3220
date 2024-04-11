#Alex Shapovalov
#CS 5220
#Programming Assignment #4, Branch Prediction

def main():
    # create branch dictionary (array was not a good idea)
    branches = {}

    filename = "curl1m.btrace.txt"
    bits = 0 # 0, 1, 2, or 3. this is N

    taken = 0
    skipped = 0
    total = 0
    prediction = 0
    predicted = 0

    printArray = ["static BP: ", "1 bit BP: ", "2 bit BP: ", "3 bit BP: "]

    # run three times, static, one-bit, two-bit, three-bit (for loop change A % N)
    for bits in range(0, 4):
        with open(filename, 'r') as file:
            for line in file:
                instruction = line.split()

                address = instruction[0]

                value = int(instruction[1])

                # if branch is new, add to dictionary
                if address not in branches:
                    branches[address] = {"taken": 0, "skipped": 0, "total": 0, "previous": 0}

                # alter prediction value based on branch prediction
                if (bits == 1):
                    prediction = branches[address]["previous"] #predict whatever the last value was

                # alter prediction based on 2 bit prediction
                elif (bits == 2):
                    if (branches[address]["previous"] in range(2, 3)):
                        prediction = 1
                    elif (branches[address]["previous"] in range(0, 1)):
                        prediction = 0

                # alter prediction based on 3 bit prediction
                elif (bits == 3):
                    if (branches[address]["previous"] in range(2, 8)):
                        prediction = 1
                    elif (branches[address]["previous"] in range(0, 1)):
                        prediction = 0

                else: # 0 bit prediction
                    prediction = 0

                # add tallies based on branch taken / not taken
                if value == 0: # not taken
                    branches[address]["skipped"] += 1
                    if (bits == 1): # single bit
                        if (prediction == 0):
                            predicted += 1
                            branches[address].update({"previous": 1})
                        else:
                            branches[address].update({"previous": 0})

                    # change based on bits
                    elif (bits == 2):
                        if (prediction == 0):
                            predicted += 1
                            branches[address]["previous"] = min(branches[address]["previous"] + 1, 3)
                        else:
                            branches[address]["previous"] = max(branches[address]["previous"] - 1, 0)

                    # change based on bits
                    elif (bits == 3):
                        if (prediction == 0):
                            predicted += 1
                            branches[address]["previous"] = min(branches[address]["previous"] + 1, 8)
                        else:
                            branches[address]["previous"] = max(branches[address]["previous"] - 1, 0)

                    else:
                        if (prediction == 0):
                            predicted += 1
                            branches[address].update({"previous": 1})

                    skipped += 1

                    # add to total
                    branches[address]["total"] = branches[address]["skipped"] + branches[address]["taken"]

                else: # taken
                    branches[address]["taken"] += 1
                    if (bits == 1):  # single bit
                        if (prediction == 1):
                            predicted += 1
                            branches[address].update({"previous": 1})
                        else:
                            branches[address].update({"previous": 0})

                    elif (bits == 2):
                        if (prediction == 1):
                            predicted += 1
                            branches[address]["previous"] = min(branches[address]["previous"] + 1, 3)
                        else:
                            branches[address]["previous"] = max(branches[address]["previous"] - 1, 0)

                    elif (bits == 3):
                        if (prediction == 1):
                            predicted += 1
                            branches[address]["previous"] = min(branches[address]["previous"] + 1, 8)
                        else:
                            branches[address]["previous"] = max(branches[address]["previous"] - 1, 0)

                    else:
                        pass

                    taken += 1

                    # add to total
                    branches[address]["total"] = branches[address]["skipped"] + branches[address]["taken"]

                total += 1
        print(printArray[bits] + str('{:.2f}'.format((predicted / total) * 100)) + "% accurate")
        print("")

        if (bits < 3):
            branches = {}

            taken = 0
            skipped = 0
            total = 0
            prediction = 0
            predicted = 0

    # totals
    print("unique branches: " + str(len(branches)) + ", total taken: " + str(taken) + ", total skipped: " + str(skipped) + ", total branches: " + str(total))

main()