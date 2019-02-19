
from .flow import Try
from .http import InternalServerError

from .challenge import twarf_rules as challenge_rules


def twarf_rules(reactor):
    return Try(
        body=challenge_rules(reactor),
        fail=InternalServerError(),
    )
