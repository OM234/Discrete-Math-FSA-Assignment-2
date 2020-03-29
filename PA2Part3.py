def minimizeDFA(states, alphabet, transitions, root, acceptingStates):

    equivalenceLists = []
    equivalenceLists = makeEquivalenceLists(equivalenceLists, states, alphabet, transitions, root, acceptingStates)
    minStates = getMinStates(equivalenceLists)
    minTransitions = getMinTransitions(minStates, transitions)
    minRoot = getMinRoot(minStates, root)
    minAcceptingStates = getMinAcceptingStates(minStates, acceptingStates)


def makeEquivalenceLists(equivalenceLists, states, alphabet, transitions, root, acceptingStates):

    equivalenceLists = getZeroEquivalence(equivalenceLists, states, acceptingStates)
    print(equivalenceLists)
    newEquivalenceList = []

    while newEquivalenceList.sort() != equivalenceLists.sort():
        if len(newEquivalenceList) > 0:
            equivalenceLists = newEquivalenceList
        newEquivalenceList = getNEquivalance(equivalenceLists, states, alphabet, transitions, root, acceptingStates)

    return equivalenceLists

def getZeroEquivalence(equivalenceLists, states, acceptingStates):

    acceptingStatesList = []
    otherStatesList = []

    for state in states:
        if state in acceptingStates:
            acceptingStatesList.append(state)
        else:
            otherStatesList.append(state)

    equivalenceLists.append(acceptingStatesList)
    equivalenceLists.append(otherStatesList)

    return equivalenceLists


def getNEquivalance(equivalenceLists, states, alphabet, transitions, root, acceptingStates):

states = ("A", "B", "C", "D", "E")
root = "A"
alphabet = ("0", "1")
acceptingStates = ("E",)
transitions = (("A", "0", "B"), ("A", "1", "C"), ("B", "0", "B"), ("B", "1", "D"), ("C", "0", "B"),
               ("C", "1", "C"), ("D", "0", "B"), ("D", "1", "E"), ("E", "0", "B"),
               ("E", "1", "C"))

minimizeDFA(states, alphabet, transitions, root, acceptingStates)