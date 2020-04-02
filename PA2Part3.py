from PySimpleAutomata import automata_IO, DFA, NFA
import TablePrinter
import os


def makeDFA():

    states = getStates()
    root = getRoot(states)
    acceptingStates = getAcceptingStates(states)
    alphabet = getAlphabet()
    transitions = getDFATransitions(states, alphabet)
    buildDFADotFile(states, alphabet, transitions, root, acceptingStates)
    minimizeDFA(states, alphabet, transitions, root, acceptingStates)


def minimizeDFA(states, alphabet, transitions, root, acceptingStates):
    equivalenceLists = []
    minStates = removeUnreachable(states, transitions, root)
    equivalenceLists = makeEquivalenceLists(equivalenceLists, minStates, alphabet, transitions, root, acceptingStates)
    minStates = getMinStates(equivalenceLists)
    minTransitions = getMinTransitions(minStates, transitions, alphabet)
    minRoot = getMinRoot(minStates, root)
    minAcceptingStates = getMinAcceptingStates(minStates, acceptingStates)
    buildDFADotFile(minStates, alphabet, minTransitions, minRoot, minAcceptingStates)
    makeDFASVGFile()
    printTable(minStates, alphabet, minTransitions, minRoot, minAcceptingStates)


def getStates():
    states = input("Enter states, seperated by a comma and space: ")
    statesList = states.split(", ")
    statesTuple = tuple(statesList)
    return statesTuple


def getRoot(states):
    print(states)
    while True:  # error checking
        root = input("Which one is the root? ")
        if root in states:
            return root


def getAcceptingStates(states):
    numOfAcceptingStates = ""
    numOfAcceptingStatesSelected = 0
    acceptingState = ""
    acceptingStatesList = []
    acceptingStatesTuple = ()

    print(states)
    while numOfAcceptingStates.isdigit() is False or int(numOfAcceptingStates) < 1:  # error checking
        numOfAcceptingStates = input("How many accepting states? ")
    while numOfAcceptingStatesSelected < int(numOfAcceptingStates):
        acceptingState = input("Which node is an accepting state? ")
        if acceptingState in states and acceptingState not in acceptingStatesList:
            acceptingStatesList.append(acceptingState)
            numOfAcceptingStatesSelected = numOfAcceptingStatesSelected + 1

    acceptingStatesTuple = tuple(acceptingStatesList)
    return acceptingStatesTuple


def getAlphabet():
    numOfSymbols = ""
    alphabetList = []
    alphabetTuple = ()

    while numOfSymbols.isdigit() is False or int(numOfSymbols) < 1:
        numOfSymbols = input("How many symbols? ")

    for i in range(int(numOfSymbols)):
        alphabetList.append(input("Symbol " + str(i + 1) + ": "))

    alphabetTuple = tuple(alphabetList)
    print(alphabetTuple)
    return alphabetTuple


def getDFATransitions(states, alphabet):
    transitionsList = []
    transitionsTuple = ()
    resultState = ""

    for state in states:
        for symbol in alphabet:
            resultState = ""
            while resultState not in states and resultState != "-":
                resultState = input("State '" + state + "' with symbol '" + symbol + "' goes to state: ")
            transition = (state, symbol, resultState)
            transitionsList.append(transition)

    transitionsTuple = tuple(transitionsList)
    return transitionsTuple


def removeUnreachable(states, transitions, root):

    initialStates = [root, ]
    resultStates = []

    while len(initialStates) > 0:
        for transition in transitions:
            if transition[0] == initialStates[0] and transition[2] not in resultStates and transition[2] not in initialStates:
                initialStates.append(transition[2])
        resultStates.append(initialStates.pop(0))

    return resultStates


def makeEquivalenceLists(equivalenceLists, states, alphabet, transitions, root, acceptingStates):
    equivalenceLists = getZeroEquivalence(equivalenceLists, states, acceptingStates)
    newEquivalenceList = []

    while newEquivalenceList != equivalenceLists:
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
    newEquivalanceLists = []

    for equivalenceList in equivalenceLists:
        for state in equivalenceList:
            equivalenceFound = False
            for newEquivalenceList in newEquivalanceLists:
                for newState in newEquivalenceList:
                    if isEquivalent(state, newState, equivalenceLists, transitions, alphabet, acceptingStates):
                        equivalenceFound = True
                        newEquivalenceList.append(state)
                        break
                    else:
                        break
                if equivalenceFound:
                    break
            if equivalenceFound is False:
                newEquivalanceLists.append([state])

    return newEquivalanceLists


def isEquivalent(state, newState, equivalenceLists, transitions, alphabet, acceptingStates):
    resultState = []
    resultNewState = []

    if newState in acceptingStates and state not in acceptingStates:
        return False
    if state in acceptingStates and newState not in acceptingStates:
        return False

    for transition in transitions:
        for symbol in alphabet:
            if transition[0] == state and transition[1] == symbol:
                resultState.append(transition[2])
            if transition[0] == newState and transition[1] == symbol:
                resultNewState.append(transition[2])

    if resultState == resultNewState:
        return True

    for equivalenceList in equivalenceLists:
        stateInList = False
        newStateInList = False
        for state in resultState:
            if state in equivalenceList:
                stateInList = True
                break
        for state in resultNewState:
            if state in equivalenceList:
                newStateInList = True
                break
        if stateInList != newStateInList:
            return False

    return True


def getMinStates(equivalenceLists):
    minStates = []

    for equivalenceList in equivalenceLists:
        newStates = []
        for states in equivalenceList:
            newStates.append(states)
        minStates.append(aggregateStates(newStates))

    return tuple(minStates)


def getMinTransitions(minStates, transitions, alphabet):
    minTransitions = []

    for state in minStates:
        for transition in getStateTransitions(state, minStates, transitions, alphabet):
            minTransitions.append(transition)

    return minTransitions


def aggregateStates(states):
    newStates = []
    newState = ""
    for state in states:
        newStates.append(state)
    newStates.sort()
    for state in newStates:
        newState = newState + "." + state
    newState = newState.replace(".", "", 1)  # remove period at beginning
    return newState


def statesComposition(state):
    states = state.split(".")

    return states


def getStateTransitions(initialState, minStates, transitions, alphabet):
    initialStatesList = statesComposition(initialState)
    transitionTable = []

    for symbol in alphabet:
        finalStateList = []
        for state in initialStatesList:
            for transition in transitions:
                if transition[0] == state and transition[1] == symbol and transition[2] not in finalStateList:
                    for aState in minStates:
                        if transition[2] in statesComposition(aState):
                            finalStateList.append(aState)
                            break
            if len(finalStateList) > 0:
                break
        if len(finalStateList) > 0:
            transitionTable.append((initialState, symbol, aggregateStates(finalStateList)))

    return transitionTable


def getMinRoot(minStates, root):
    for state in minStates:
        if root in statesComposition(state):
            return state


def getMinAcceptingStates(minStates, acceptingStates):
    newAcceptingStates = []

    for state in minStates:
        for acceptingState in acceptingStates:
            if acceptingState in statesComposition(state) and state not in newAcceptingStates:
                newAcceptingStates.append(state)

    return newAcceptingStates


def buildDFADotFile(states, alphabet, transitions, roots, acceptingStates):
    dotFile = open("PA2.dot", "+w")

    dotFile.write("digraph{\n\t")

    for state in states:
        dotFile.write(state)
        if state in roots and state in acceptingStates:
            dotFile.write(" [root=true, shape=doublecircle]")
        elif state in roots:
            dotFile.write(" [root=true]")
        elif state in acceptingStates:
            dotFile.write(" [shape=doublecircle]")
        dotFile.write("\n\t")

    for transition in transitions:
        dotFile.write(transition[0] + " -> " + transition[2] + " [label=\"" + transition[1] + "\"]\n\t")

    dotFile.write("}")
    return dotFile


def makeDFASVGFile():
    os.environ["PATH"] += os.pathsep + 'D:/Program Files (x86)/Graphviz2.38/bin/'
    dfa_example = automata_IO.dfa_dot_importer("PA2.dot")
    automata_IO.dfa_to_dot(dfa_example, "DFA",
                           r"D:/School/Concordia - Graduate Diploma in Computer Science/COMP 5361 - "
                           r"Discrete Structures and Formal Languages/Programming Assignment 2")


def printTable(DFAStates, alphabet, DFATransitionTable, DFARoot, DFAAcceptingStates):
    DFARoot = (DFARoot,)
    TablePrinter.generateTable(DFAStates, alphabet, DFATransitionTable, DFARoot, DFAAcceptingStates)


makeDFA()

'''
states = ("A", "B", "C", "D", "E")
root = "A"
alphabet = ("0", "1")
acceptingStates = ("E",)
transitions = (("A", "0", "B"), ("A", "1", "C"), ("B", "0", "B"), ("B", "1", "D"), ("C", "0", "B"),
               ("C", "1", "C"), ("D", "0", "B"), ("D", "1", "E"), ("E", "0", "B"),
               ("E", "1", "C"))
'''

'''
states = ("q0", "q1", "q2", "q3", "q4", "q5")
root = "q0"
alphabet = ("0", "1")
acceptingStates = ("q3", "q5")
transitions = (("q0", "0", "q1"), ("q0", "1", "q3"), ("q1", "0", "q0"), ("q1", "1", "q3"),
               ("q2", "0", "q1"), ("q2", "1", "q4"), ("q3", "0", "q5"), ("q3", "1", "q5"),
               ("q4", "0", "q3"), ("q4", "1", "q3"), ("q5", "0", "q5"), ("q5", "1", "q5"),
               )
'''