"""
TODO: Cross machine communication
"""
import contextlib
from functools import wraps
from typing import Generator

from pyfsm.exceprions import UnreleasedTransition


class State:

    def __init__(self, state_generator: Generator) -> None:
        assert state_generator
        self._state_generator: Generator = state_generator
        self.state_name = state_generator.gi_code.co_name

    def __eq__(self, other):
        if not isinstance(other, (self.__class__,)):
            other_class = other.__class__
            raise TypeError(f'unsupported operand type(s): {other_class}')
        return self.state_name == other.state_name

    def __ne__(self, other):
        if not isinstance(other, (self.__class__,)):
            other_class = other.__class__
            raise TypeError(f'unsupported operand type(s): {other_class}')
        return self.state_name != other.state_name

    def init(self):
        next(self._state_generator)

    def next(self, proposed_state = None):
        if not isinstance(proposed_state, self.__class__):
            TypeError(f'state must be instance of {self.__class__}')
        with contextlib.suppress(StopIteration):
            self._state_generator.send(proposed_state)
            next(self._state_generator)


def as_state(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        generator = func(self, *args, **kwargs)
        return self.state_class(generator)
    return wrapper


class FSM:
    """State machine class.

       To implement new state you should create generator-method with single
       yield operator.

       Code before yield is initiation of state - you can check any conditions
       you need and raise UnreleasedTransition if requirements for transition
       not be met. Leave empty to pass by.

       Code after yield is for transition to another state.
       Leave empty to stop (it wil be finite state)
       """
    state = None
    state_class = State

    def __init__(self) -> None:
        """Init of state-machine."""
        self.set_state(self.initial_state())

    def set_state(self, state: State):
        """Set state-machine to state.

        :param state: State object
        """
        if not isinstance(state, State):
            raise TypeError(f'state must be instance of {State}')
        # If UnreleasedTransition will raised the state remains unchanged
        with contextlib.suppress(UnreleasedTransition):
            # Trying to init new state
            state.init()
            self.state = state

    def next_state(self, proposed_state=None):
        """Transition not next state.

        Transition not next state or trying to process proposed state if
        if it necessary. Anyway proposed_state will be send to yield of state.
        :param proposed_state: State object
        """
        if not isinstance(proposed_state, State):
            TypeError(f'state must be instance of {State}')
        self.state.next(proposed_state)

    @as_state
    def initial_state(self):
        """Initial state.

        This it always first state of state-machine.
        And it always must to generator.
        """

        # Initial code for state
        yield
        # Code for transition to state. It makes with set_state method
