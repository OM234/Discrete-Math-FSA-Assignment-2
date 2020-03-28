from PySimpleAutomata import automata_IO, DFA, NFA
import os


def isDFA():  # true if DFA, false if NFA

    while True:  # error checking
        DFAorNFA = input("Is this a DFA or NFA? ")
        if DFAorNFA == "DFA":
            return True
        elif DFAorNFA == "NFA":
            return False


def makeFSA(isADFA):

    if isADFA:
        makeDFA()
    else:
        makeNFA()


def makeDFA():

    states = getStates()
    root = getRoot(states)
    acceptingStates = getAcceptingStates(states)
    alphabet = getAlphabet()
    transitions = getDFATransitions(states, alphabet)
    buildDFADotFile(states, alphabet, transitions, root, acceptingStates)


def makeNFA():

    states = getStates()
    roots = getRoots(states)
    acceptingStates = getAcceptingStates(states)
    alphabet = getAlphabet()
    transitions = getNFATransitions(states, alphabet)
    buildNFADotFile(states, alphabet, transitions, roots, acceptingStates)


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


def getRoots(states):

    numOfRoots = ""
    numOfRootsSelected = 0
    root = ""
    rootsList = []
    rootsTuple = ()

    print(states)
    while numOfRoots.isdigit() is False or int(numOfRoots) < 1:  # error checking
        numOfRoots = input("How many roots? ")
    while numOfRootsSelected < int(numOfRoots):
        root = input("Which node is a root? ")
        if root in states and root not in rootsList:
            rootsList.append(root)
            numOfRootsSelected = numOfRootsSelected + 1

    rootsTuple = tuple(rootsList)
    return rootsTuple


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
        alphabetList.append(input("Symbol " + str(i+1) + ": "))

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


def getNFATransitions(states, alphabet):

    transitionsList = []
    transitionsTuple = ()
    numTransitions = ""

    while numTransitions.isdigit() is False or int(numTransitions) < 1:
        numTransitions = input("How many transitions? ")

    for i in range(int(numTransitions)):

        state = ""
        resultState = ""
        transitionSymbol = ""

        print("\ntransition #" + str(i + 1))

        while state not in states:
            state = input("Initial state: ")

        while transitionSymbol not in alphabet:
            transitionSymbol = input("Transition symbol: ")

        while resultState not in states:
            resultState = input("Result state: ")

        transition = (state, transitionSymbol, resultState)
        transitionsList.append(transition)

    transitionsTuple = tuple(transitionsList)
    print(transitionsTuple)
    return transitionsTuple


def buildDFADotFile(states, alphabet, transitions, root, acceptingStates):

    dotFile = open("PA2.dot", "+w")

    dotFile.write("digraph{\n\t")

    for state in states:
        dotFile.write(state)
        if state == root and state in acceptingStates:
            dotFile.write(" [root=true, shape=doublecircle]")
        elif state == root:
            dotFile.write(" [root=true]")
        elif state in acceptingStates:
            dotFile.write(" [shape=doublecircle]")
        dotFile.write("\n\t")

    for transition in transitions:
        dotFile.write(transition[0] + " -> " + transition[2] + " [label=\"" + transition[1] + "\"]\n\t")

    dotFile.write("}")
    return dotFile


def buildNFADotFile(states, alphabet, transitions, roots, acceptingStates):

    pass


isADFA = isDFA()
makeFSA(isADFA)

if isADFA:
    os.environ["PATH"] += os.pathsep + 'D:/Program Files (x86)/Graphviz2.38/bin/'
    dfa_example = automata_IO.dfa_dot_importer("PA2.dot")
    automata_IO.dfa_to_dot(dfa_example, "DFA", r"D:/School/Concordia - Graduate Diploma in Computer Science/COMP 5361 - "
                                           r"Discrete Structures and Formal Languages/Programming Assignment 2")

if not isADFA:
    os.environ["PATH"] += os.pathsep + 'D:/Program Files (x86)/Graphviz2.38/bin/'
    nfa_example = automata_IO.nfa_dot_importer("PA2.dot")
    automata_IO.nfa_to_dot(nfa_example, "NFA",
                           r"D:/School/Concordia - Graduate Diploma in Computer Science/COMP 5361 - "
                           r"Discrete Structures and Formal Languages/Programming Assignment 2")