def generateTable(states, alphabet, transitions, roots, acceptingStates):

    trapState = False

    for row in range(len(states) + 1):
        if row == 0:  # header
            print("{:>13}".format("|"), end="")
            for symbol in alphabet:
                print("{:^10}|".format(symbol), end="")
            print("\n-------------" + "-----------"*len(alphabet))
        else:
            for column in range(len(alphabet) + 1):
                if column == 0:
                    if states[row - 1] in roots:
                        print("-->{:^9}|".format(states[row - 1]), end="")
                    elif states[row - 1] in acceptingStates:
                        print("{:^12}|".format("*" + states[row - 1]), end="")
                    else:
                        print("{:^12}|".format(states[row - 1]), end="")

                else:
                    resultState = getTransitionResult(states[row - 1], alphabet[column-1], transitions)
                    if resultState == "TRP":
                        trapState = True
                    print("{:^10}|".format(resultState), end="")
            print("\n-------------" + "-----------" * len(alphabet))

    if trapState:
        for column in range(len(alphabet) + 1):
            if column == 0:
                print("{:^12}|".format("TRP"), end="")
            else:
                print("{:^10}|".format("TRP"), end="")
        print("\n-------------" + "-----------" * len(alphabet))


def getTransitionResult(initialState, symbol, transitions):

    for transition in transitions:
        if initialState == transition[0] and symbol == transition[1]:
            return transition[2]

    return "TRP"




'''
states = ("AAAAA", "BBBBBB", "CCCCCC")
roots = ("AAAAA",)
alphabet = ("a", "b", "c")
acceptingStates = ("CCCCCC",)
transitions = (("AAAAA", "b", "AAAAA"), ("BBBBBB", "c", "BBBBBB"), ("BBBBBB", "c", "BBBBBB"))
generateTable(states, alphabet, transitions, roots, acceptingStates)
'''