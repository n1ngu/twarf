
import os

import twarf.rules.forward
import twarf.service.session


def twarf_rules(reactor):
    session_service = twarf.service.session.SessionService()
    forward = twarf.rules.forward.AForward(
        reactor,
        os.environ['TWARF_FORWARD_HOST'],
        int(os.environ['TWARF_FORWARD_PORT'])
    )
    set_cookie = twarf.service.session.SetCookie(
        session_service,
        forward
    )
    return set_cookie.process
