import pytest

from tests import machine


@pytest.fixture()
def simple_fsm():
    return machine.SimpleFSM()


@pytest.fixture()
def linear_fsm():
    return machine.LinearFSM()


@pytest.fixture()
def cycle_fsm():
    return machine.CycleFSM()


@pytest.fixture()
def proposal_fsm():
    return machine.ProposalFSM()
