from PySimpleAutomata import automata_IO, DFA, NFA
import TablePrinter
import os


def makeDFA():
    NFAStates = getNFAStates()
    NFARoots = getRoots(NFAStates)
    NFAAcceptingStates = getAcceptingStates(NFAStates)
    alphabet = getAlphabet()
    NFATransitions = getNFATransitions(NFAStates, alphabet)
    DFATransitionTable = buildDFATable(NFAStates, alphabet, NFATransitions, NFARoots, NFAAcceptingStates)
    DFAStates = getDFAStates(DFATransitionTable)
    DFARoot = getDFARoot(DFATransitionTable, NFARoots)
    DFAAcceptingStates = getDFAAcceptingStates(DFAStates, NFAAcceptingStates)
    buildDFADotFile(DFAStates, alphabet, DFATransitionTable, DFARoot, DFAAcceptingStates)
    makeDFASVGFile()
    printTable(DFAStates, alphabet, DFATransitionTable, DFARoot, DFAAcceptingStates)


def getNFAStates():
    states = input("Enter states, seperated by a comma and space: ")
    statesList = states.split(", ")
    statesTuple = tuple(statesList)
    return statesTuple

def getDFAStates(DFATransitionTable):

    DFAStates = []

    for transition in DFATransitionTable:
        if transition[0] not in DFAStates:
            DFAStates.append(transition[0])
        if transition[2] not in DFAStates:
            DFAStates.append(transition[2])

    return DFAStates


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
        alphabetList.append(input("Symbol " + str(i + 1) + ": "))

    alphabetTuple = tuple(alphabetList)
    print(alphabetTuple)
    return alphabetTuple


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
    return transitionsTuple


def buildDFATable(states, alphabet, NFATransitions, roots, acceptingStates):
    DFATransitionsInitial = []  # each table will be a tuple with 3 elements: initial state, transition, final state
    DFATransitionsFinal = []

    DFATransitionsInitial = populateDFATransitionsInitalWithRoots(DFATransitionsInitial, roots, NFATransitions,
                                                                  alphabet)
    DFATransitionsFinal = iterateThroughTables(DFATransitionsInitial, DFATransitionsFinal, NFATransitions, alphabet)

    return DFATransitionsFinal


def populateDFATransitionsInitalWithRoots(DFATransitionsInitial, roots, NFATransitions, alphabet):
    rootsList = []

    for root in roots:
        rootsList.append(root)

    aggregateRoot = aggregateStates(rootsList)
    DFATransitionsInitial = getStateTransition(aggregateRoot, NFATransitions, alphabet)
    return DFATransitionsInitial


def aggregateStates(states):
    '''newStates = ""

    for state in states:
        newStates = newStates + "." + state
    newStates = newStates.replace(".", "", 1)  # remove comma at beginning
    return newStates
    '''
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


def getStateTransition(initialState, NFATransitions, alphabet):
    initialStatesList = statesComposition(initialState)
    transitionTable = []

    for symbol in alphabet:
        finalStateList = []
        for state in initialStatesList:
            for transition in NFATransitions:
                if transition[0] == state and transition[1] == symbol and transition[2] not in finalStateList:
                    finalStateList.append(transition[2])
        if len(finalStateList) > 0:
            transitionTable.append((initialState, symbol, aggregateStates(finalStateList)))

    return transitionTable


def iterateThroughTables(DFATransitionsInitial, DFATransitionsFinal, NFATransitions, alphabet):
    while len(DFATransitionsInitial) > 0:

        newTransition = getStateTransition(DFATransitionsInitial[0][2], NFATransitions, alphabet)
        for transition in newTransition:
            if transition not in DFATransitionsFinal:
                DFATransitionsInitial.append(transition)
        if DFATransitionsInitial[0] not in DFATransitionsFinal:
            DFATransitionsFinal.append(DFATransitionsInitial[0])
        DFATransitionsInitial.pop(0)

    return DFATransitionsFinal


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


def getDFARoot(DFATransitionTable, NFARoots):

    for transition in DFATransitionTable:
        states = transition[0]
        for state in statesComposition(states):
            if state in NFARoots:
                return states


def getDFAAcceptingStates(DFAStates, NFAAcceptingStates):

    DFAAcceptingStates = []

    for stateAggregate in DFAStates:
        for state in statesComposition(stateAggregate):
            if state in NFAAcceptingStates and stateAggregate not in DFAAcceptingStates:
                DFAAcceptingStates.append(stateAggregate)

    return tuple(DFAAcceptingStates)


def makeDFASVGFile():

    os.environ["PATH"] += os.pathsep + 'D:/Program Files (x86)/Graphviz2.38/bin/'
    dfa_example = automata_IO.dfa_dot_importer("PA2.dot")
    DFA.dfa_completion(dfa_example)
    DFA.dfa_minimization(dfa_example)
    automata_IO.dfa_to_dot(dfa_example, "DFA", r"D:/School/Concordia - Graduate Diploma in Computer Science/COMP 5361 - "
                                           r"Discrete Structures and Formal Languages/Programming Assignment 2")


def printTable(DFAStates, alphabet, DFATransitionTable, DFARoot, DFAAcceptingStates):

    DFARoot = (DFARoot,)
    TablePrinter.generateTable(DFAStates, alphabet, DFATransitionTable, DFARoot, DFAAcceptingStates)


makeDFA()
