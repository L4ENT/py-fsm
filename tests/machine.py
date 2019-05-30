import pyfsm


class SimpleFSM(pyfsm.FSM):
    """Simple finite state machine."""

    @pyfsm.as_state
    def initial_state(self):
        yield
        self.set_state(self.first_state())

    @pyfsm.as_state
    def first_state(self):
        yield
        self.set_state(self.second_state())

    @pyfsm.as_state
    def second_state(self):
        self.set_state(self.first_state())
        proposed_state = yield
        # if proposal state passed set it else finite state
        if proposed_state:
            self.set_state(proposed_state)
        else:
            self.set_state(self.final_state())

    @pyfsm.as_state
    def final_state(self):
        yield


class LinearFSM(pyfsm.FSM):
    """Linear finite state machine."""

    @pyfsm.as_state
    def initial_state(self):
        yield
        self.set_state(self.first_state())

    @pyfsm.as_state
    def first_state(self):
        yield
        self.set_state(self.second_state())

    @pyfsm.as_state
    def second_state(self):
        yield
        self.set_state(self.final_state())

    @pyfsm.as_state
    def final_state(self):
        yield


class CycleFSM(pyfsm.FSM):
    """Cycle finite state machine."""

    @pyfsm.as_state
    def initial_state(self):
        # Entry point
        yield
        self.set_state(self.ping_state())

    @pyfsm.as_state
    def ping_state(self):
        yield
        self.set_state(self.pong_state())

    @pyfsm.as_state
    def pong_state(self):
        yield
        self.set_state(self.ping_state())


class ProposalFSM(pyfsm.FSM):
    """Proposal finite state machine."""

    def __init__(self) -> None:
        super().__init__()

        self.current_direction = None

        self._available_states = [
            self.left_direction(),
            self.right_direction(),
            self.forward_direction(),
            self.back_direction(),
            self.stop()
        ]

    def set_proposal_state(self, state):
        if state in self._available_states:
            self.set_state(state)
        else:
            raise pyfsm.UnreleasedTransition()

    @pyfsm.as_state
    def initial_state(self):
        proposal_state = yield
        self.set_state(proposal_state)

    @pyfsm.as_state
    def left_direction(self):
        self.current_direction = 'left'
        proposal_state = yield
        self.set_proposal_state(proposal_state)

    @pyfsm.as_state
    def right_direction(self):
        self.current_direction = 'right'
        proposal_state = yield
        self.set_proposal_state(proposal_state)

    @pyfsm.as_state
    def forward_direction(self):
        self.current_direction = 'forward'
        proposal_state = yield
        self.set_proposal_state(proposal_state)

    @pyfsm.as_state
    def back_direction(self):
        self.current_direction = 'back'
        proposal_state = yield
        self.set_proposal_state(proposal_state)

    @pyfsm.as_state
    def stop(self):
        self.current_direction = 'stop'
        proposal_state = yield
        self.set_proposal_state(proposal_state)
