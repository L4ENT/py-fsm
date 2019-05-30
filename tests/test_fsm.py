from itertools import cycle, islice
from random import randint

import pytest

import pyfsm
from tests import machine


def test_simple_fsm(simple_fsm: machine.SimpleFSM):
    """Test simple FSM."""
    # Initial step by default
    assert simple_fsm.state == simple_fsm.initial_state()
    # To first state
    simple_fsm.next_state()
    assert simple_fsm.state == simple_fsm.first_state()
    # To second state
    simple_fsm.next_state()
    assert simple_fsm.state == simple_fsm.second_state()
    # Again to initial and do second round
    simple_fsm.next_state(simple_fsm.initial_state())
    assert simple_fsm.state == simple_fsm.initial_state()
    # To first state
    simple_fsm.next_state()
    assert simple_fsm.state == simple_fsm.first_state()
    # To second state
    simple_fsm.next_state()
    assert simple_fsm.state == simple_fsm.second_state()
    # To second final state
    simple_fsm.next_state()
    assert simple_fsm.state == simple_fsm.final_state()


def test_linear_fsm(linear_fsm: machine.LinearFSM):
    """Test linear FSM."""
    expected_states = [
        linear_fsm.initial_state(),
        linear_fsm.first_state(),
        linear_fsm.second_state(),
        linear_fsm.final_state(),
    ]

    real_states = []
    for _ in expected_states:
        real_states.append(linear_fsm.state)
        linear_fsm.next_state()

    assert expected_states == real_states


def test_cycle_fsm(cycle_fsm: machine.CycleFSM):
    """Test cycle FSM."""
    states_round = [cycle_fsm.ping_state(), cycle_fsm.pong_state()]
    cyclic_states_iterator = cycle(states_round)

    expected_states = [cycle_fsm.initial_state()]
    real_states = [cycle_fsm.state]

    for state in islice(cyclic_states_iterator, randint(2, 7)):
        expected_states.append(state)
        cycle_fsm.next_state()
        real_states.append(cycle_fsm.state)

    assert expected_states == real_states


def test_proposal_fsm(proposal_fsm: machine.ProposalFSM):
    """Test cycle FSM."""
    assert proposal_fsm.current_direction is None

    proposal_fsm.next_state(proposal_fsm.left_direction())
    assert proposal_fsm.current_direction == 'left'

    proposal_fsm.next_state(proposal_fsm.right_direction())
    assert proposal_fsm.current_direction == 'right'

    proposal_fsm.next_state(proposal_fsm.forward_direction())
    assert proposal_fsm.current_direction == 'forward'

    proposal_fsm.next_state(proposal_fsm.back_direction())
    assert proposal_fsm.current_direction == 'back'

    proposal_fsm.next_state(proposal_fsm.stop())
    assert proposal_fsm.current_direction == 'stop'

    with pytest.raises(pyfsm.UnreleasedTransition):
        proposal_fsm.next_state(proposal_fsm.initial_state())
    assert proposal_fsm.state == proposal_fsm.stop()
