from PySimpleAutomata import automata_IO, DFA, NFA
import os

def makeDFA():

    states = getStates()
    roots = getRoots(states)
    acceptingStates = getAcceptingStates(states)
    alphabet = getAlphabet()
    NFATransitions = getNFATransitions(states, alphabet)
    DFATransitionTable = buildDFATable(states, alphabet, NFATransitions, roots, acceptingStates)
    #buildNFADotFile(states, alphabet, transitions, roots, acceptingStates)


def getStates():

    states = input("Enter states, seperated by a comma and space: ")
    statesList = states.split(", ")
    statesTuple = tuple(statesList)
    return statesTuple


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

    DFATransitionsInitial = populateDFATransitionsInitalWithRoots(DFATransitionsInitial, roots, NFATransitions, alphabet)
    DFATransitionsFinal = iterateThroughTables(DFATransitionsInitial, DFATransitionsFinal)

    return DFATransitionsFinal


def populateDFATransitionsInitalWithRoots(DFATransitionsInitial, roots, NFATransitions, alphabet):

    rootsList = []

    for root in roots:
        rootsList.append(root)

    aggregateRoot = aggregateStates(rootsList)
    DFATransitionsInitial = getStateTransition(aggregateRoot, NFATransitions, alphabet)
    return DFATransitionsInitial


def aggregateStates(states):

    newStates = ""

    for state in states:
        newStates = newStates + "," + state
    newStates = newStates.replace(",", "", 1) # remove comma at beginning
    return newStates


def statesComposition(state):

    states = state.split(",")

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


def iterateThroughTables(DFATransitionsInitial, DFATransitionsFinal):

    while len(DFATransitionsInitial) > 0:

makeDFA()