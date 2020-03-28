from PySimpleAutomata import automata_IO, DFA
import os


os.environ["PATH"] += os.pathsep + 'D:/Program Files (x86)/Graphviz2.38/bin/'

athing = automata_IO.dfa_dot_importer("PA2.dot")
DFA.dfa_completion(athing)
new_dfa = DFA.dfa_minimization(athing)
automata_IO.dfa_to_dot(athing, "afa", r"D:/School/Concordia - Graduate Diploma in Computer Science/COMP 5361 - Discrete Structures and Formal Languages/Programming Assignment 2")
