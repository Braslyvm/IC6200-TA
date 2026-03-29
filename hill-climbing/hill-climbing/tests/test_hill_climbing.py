import copy

import hc
import utils


def test_hill_climbing_reduces_cost_on_simple_line_map():
    board = [[utils.OBJECT_HOSPITAL, None, None, None, utils.OBJECT_HOUSE]]
    before = copy.deepcopy(board)
    initial_cost = utils.cost(board)

    solved = hc.hill_climbing(board)

    assert board == before
    assert utils.cost(solved) < initial_cost
    assert solved == [[None, None, None, utils.OBJECT_HOSPITAL, utils.OBJECT_HOUSE]]


def test_hill_climbing_stops_at_local_optimum():
    board = [
        [None, utils.OBJECT_HOUSE, None],
        [utils.OBJECT_HOUSE, utils.OBJECT_HOSPITAL, utils.OBJECT_HOUSE],
        [None, utils.OBJECT_HOUSE, None],
    ]

    solved = hc.hill_climbing(copy.deepcopy(board))
    solved_cost = utils.cost(solved)

    for hospital in utils.find_objects(solved, utils.OBJECT_HOSPITAL):
        for candidate_move in utils.actions(solved, hospital):
            candidate_map = utils.result(solved, hospital, candidate_move)
            assert utils.cost(candidate_map) >= solved_cost


def test_hill_climbing_does_not_mutate_input_map_when_improvement_exists():
    board = [[utils.OBJECT_HOSPITAL, None, utils.OBJECT_HOUSE]]
    before = copy.deepcopy(board)

    solved = hc.hill_climbing(board)

    assert board == before
    assert solved != before
