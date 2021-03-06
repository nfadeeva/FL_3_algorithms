from trans_closure import *
from bottom_up import *
from gll import *
from utils import parse_graph
import os


BOTTOM_UP = True
TRANS_CLOSURE = True
GLL = True
NUM = 11
Q1_ = True
Q2_ = True


def helper_function(grammar_hom, grammar_automata, graph_name, right_result,
                    func_hom = lambda x: set(filter(lambda x: x[1]=='S',x[0])) == x[1],
                    func_automata = lambda x: set(x[0])==x[1]):
    G_hom = parse_grammar_hom(grammar_hom)
    G_automata = parse_grammar_automata(grammar_automata)

    if TRANS_CLOSURE:
        result_closure = trans_closure(parse_graph(graph_name), G_hom)
        assert func_hom((result_closure, right_result))
        print("test for {grammar_hom} and {graph_name}"
              " - trans_closure - OK"
              .format(grammar_hom=os.path.basename(grammar_hom),
                      graph_name=os.path.basename(graph_name)))
        print()

    if BOTTOM_UP:
        result_bottom_up = bottom_up(parse_graph(graph_name), G_automata)
        assert func_automata((result_bottom_up,right_result))
        print("test for {grammar_automata} and {graph_name}"
              " - bottom_up - OK"
              .format(grammar_automata=os.path.basename(grammar_automata),
                      graph_name=os.path.basename(graph_name)))
        print()

    if GLL:
        result_gll = gll(parse_graph(graph_name), G_automata)
        assert func_automata((result_gll,right_result))
        print("test for {grammar_automata} and {graph_name}"
              " - gll - OK"
              .format(grammar_automata=os.path.basename(grammar_automata),
                      graph_name=os.path.basename(graph_name)))
        print()


def test_my_example_0():
    right_result = {(0, 'S1', 0), (0, 'S5', 0),
                    (0, 'S', 0), (0, 'S3', 1),
                    (0, 'S', 2), (0, 'S6', 2),
                    (1, 'S5', 0), (1, 'S3', 2),
                    (1, 'S', 2), (1, 'S6', 2),
                    (2, 'S2', 0), (2, 'S4', 2)}

    grammar_hom = "data/grammars/grammar_hom_0"
    grammar_automata = "data/grammars/grammar_automata_0"
    graph_name = "data/graphs/graph_0"
    helper_function(grammar_hom, grammar_automata, graph_name, right_result,
                    func_hom = lambda x: set(x[0])==x[1])


# grammar with cycle and the same graph (1^*2)
def test_my_example_1():
    right_result = {(0, 'S', 1)}
    grammar_hom = "data/grammars/grammar_hom_1"
    grammar_automata = "data/grammars/grammar_automata_1"
    graph_name = "data/graphs/graph_1"
    helper_function(grammar_hom, grammar_automata, graph_name, right_result,
                    func_automata=lambda x: set(filter(lambda x: x[1]=='S',x[0])) == x[1])


# grammar with cycle and linear graph (S-> S S S, S-> S S, S->a + a->a->a->a)
def test_my_example_2():
    right_result = {(0, 'S', 1), (0, 'S', 2),(0, 'S', 3),
                    (1, 'S', 2), (1, 'S', 3),
                    (2, 'S', 3)
                    }
    grammar_hom = "data/grammars/grammar_hom_3"
    grammar_automata = "data/grammars/grammar_automata_3"
    graph_name = "data/graphs/graph_2"
    helper_function(grammar_hom, grammar_automata, graph_name, right_result)

# grammar with cycle and graph with the cycle
def test_my_example_4():
    right_result = {(0, 'S', 0),(0, 'S', 1), (0, 'S', 2),(0, 'S', 3),
                    (1, 'S', 0), (1, 'S', 1),(1, 'S', 2), (1, 'S', 3),
                    (2, 'S', 0), (2, 'S', 1), (2, 'S', 2), (2, 'S', 3),
                    (3, 'S', 0), (3, 'S', 1), (3, 'S', 2), (3, 'S', 3)

                    }
    grammar_hom = "data/grammars/grammar_hom_3"
    grammar_automata = "data/grammars/grammar_automata_3"
    graph_name = "data/graphs/graph_3"
    helper_function(grammar_hom, grammar_automata, graph_name, right_result)

# grammar a^nb^n and graph with to coprime cycles
def test_my_example_5():
    right_result = (2, 'S', 2)
    grammar_hom = "data/grammars/grammar_hom_4"
    grammar_automata = "data/grammars/grammar_automata_4"
    graph_name = "data/graphs/graph_4"
    helper_function(grammar_hom, grammar_automata, graph_name, right_result,
                    func_hom=lambda x: x[1] in x[0],
                    func_automata = lambda x: x[1] in x[0])

# grammar with eps
def test_my_example_3():
    right_result = {(0, 'S', 0), (0, 'S', 1),(1, 'S', 1)}
    grammar_hom = "data/grammars/grammar_hom_2"
    grammar_automata = "data/grammars/grammar_automata_2"
    graph_name = "data/graphs/graph_5"
    helper_function(grammar_hom, grammar_automata, graph_name, right_result)


def test_doc_graphs():
    with open('data/data_for_tests/graphs') as f:
        graphs = ['data/graphs/data/'+ x for x in f.read().splitlines()]

    if Q1_:
        # q1
        with open('data/data_for_tests/q1_answers') as f:
            right_q1 = [int(x) for x in f.read().splitlines()]

        Q1_hom = parse_grammar_hom('data/grammars/Q1_hom')
        Q1_automata= parse_grammar_automata('data/grammars/Q1_automata')

        graphs = graphs[:NUM]
        right_q1= right_q1[:NUM]

        for graph, answer in zip(graphs, right_q1):
            print("start test for {graph} and {grammar}".format(
                graph=os.path.basename(graph), grammar='Q1'))
            if TRANS_CLOSURE:
                res = trans_closure(parse_graph(graph), Q1_hom)
                assert (len(list(filter(lambda x: x[1] == 'S', res)))) == answer
                print("test for {graph} and {grammar}- trans_closure OK".format(
                    graph=os.path.basename(graph), grammar='Q1'))
                print()

            if BOTTOM_UP:
                res = bottom_up(parse_graph(graph), Q1_automata)
                assert (len(list(filter(lambda x: x[1] == 'S', res)))) == answer
                print("test for {graph} and {grammar}- bottom_up OK".format(
                    graph=os.path.basename(graph), grammar='Q1'))
                print()

            if GLL:
                res = gll(parse_graph(graph), Q1_automata)
                assert (len(list(filter(lambda x: x[1] == 'S', res)))) == answer
                print("test for {graph} and {grammar} - gll OK".format(
                    graph=os.path.basename(graph), grammar='Q1'))
                print()

    if Q2_:
        # q2
        with open('data/data_for_tests/q2_answers') as f:
            right_q2 = [int(x) for x in f.read().splitlines()]
        Q2_hom = parse_grammar_hom('data/grammars/Q2_hom')
        Q2_automata = parse_grammar_automata('data/grammars/Q2_automata')

        graphs = graphs[:NUM]
        right_q2= right_q2[:NUM]
        for graph, answer in zip(graphs, right_q2):

            if TRANS_CLOSURE:
                res = trans_closure(parse_graph(graph), Q2_hom)
                print("start test for {graph} and {grammar}".format(
                    graph=os.path.basename(graph), grammar='Q2'))
                assert (len(list(filter(lambda x: x[1] == 'S', res)))) == answer
                print("test for {graph} and {grammar}- trans_closure OK".format(
                    graph=os.path.basename(graph), grammar='Q2'))
                print()


            if BOTTOM_UP:
                res = bottom_up(parse_graph(graph), Q2_automata)
                assert (len(list(filter(lambda x: x[1] == 'S', res)))) == answer
                print("test for {graph} and {grammar}- bottom_up OK".format(
                    graph=os.path.basename(graph), grammar='Q2'))
                print()


            if GLL:
                res = gll(parse_graph(graph), Q2_automata)
                assert (len(list(filter(lambda x: x[1] == 'S', res)))) == answer
                print("test for {graph} and {grammar} - gll OK".format(
                    graph=os.path.basename(graph), grammar='Q2'))
                print()
