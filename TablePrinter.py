def generateTable(states, alphabet, transitions, roots, acceptingStates):

    trapState = False

    for row in range(len(states) + 1):
        if row == 0:  # header
            print("{:>8}".format("|"), end="")
            for symbol in alphabet:
                print("{:^5}|".format(symbol), end="")
            print("\n--------" + "------"*len(alphabet))
        else:
            for column in range(len(alphabet) + 1):
                if column == 0:
                    if states[row - 1] in roots:
                        print("-->{:^4}|".format(states[row - 1]), end="")
                    elif states[row - 1] in acceptingStates:
                        print("{:^7}|".format("*" + states[row - 1]), end="")
                    else:
                        print("{:^7}|".format(states[row - 1]), end="")

                else:
                    resultState = getTransitionResult(states[row - 1], alphabet[column-1], transitions)
                    if resultState == "TRP":
                        trapState = True
                    print("{:^5}|".format(resultState), end="")
            print("\n--------" + "------" * len(alphabet))

    if trapState:
        for column in range(len(alphabet) + 1):
            if column == 0:
                print("{:^7}|".format("TRP"), end="")
            else:
                print("{:^5}|".format("TRP"), end="")
        print("\n--------" + "------" * len(alphabet))


def getTransitionResult(initialState, symbol, transitions):

    for transition in transitions:
        if initialState == transition[0] and symbol == transition[1]:
            return transition[2]

    return "TRP"




'''
states = ("A", "B", "C")
roots = ("A",)
alphabet = ("a", "b", "c")
acceptingStates = ("C",)
transitions = (("A", "b", "C"), ("A", "c", "A"), ("B", "c", "B"), ("C", "c", "D"))
generateTable(states, alphabet, transitions, roots, acceptingStates)
'''