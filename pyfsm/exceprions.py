import json


class UnreleasedTransition(Exception):
    """It reports that the state transition cannot be performed."""

    def __init__(self, message: str = None, errors: object = None) -> None:
        self.message = message
        self.errors = errors
        args = [message] if message else []
        super(UnreleasedTransition, self).__init__(*args)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'message': self.message,
            'errors': self.errors
        }


class ProposalStatesForbidden(UnreleasedTransition):
    """If trying to set state forcefully when it forbidden."""
