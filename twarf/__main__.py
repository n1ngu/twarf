
import sys
import argparse
import logging.config

import twisted.internet.reactor
# from twisted.web import proxy, server
import twisted.web.server

import twarf.proxy


def _logging_cfg(verbosity: int):
    return {
        'version': 1,
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'INFO',
            },
            'twarf': {
                'handlers': ['null'],
                'level': 'DEBUG' if verbosity else 'INFO',
                'propagate': True,
                'qualname': 'twarf',
            },
        },
        'handlers': {
            'console': {
                'formatter': 'debug' if verbosity else 'default',
                'class': 'logging.StreamHandler',
                'stream': sys.stdout,
            },
            'null': {
                'formatter': 'default',
                'class': 'logging.NullHandler',
            },
        },
        'formatters': {
            'default': {
                'format':
                    '%(levelname)s:%(name)s:%(message)s',
            },
            'debug': {
                'format':
                    '%(asctime)s.%(msecs)03d %(levelname)s '
                    '[%(name)s:%(funcName)s #%(lineno)s] %(message)s',
                'datefmt': '%H:%M:%S',
            },
        },
    }


def _get_parser():
    def ipv4_port_type(port: str) -> int:
        x = int(port)
        if x > 65535 or x < 0:
            raise argparse.ArgumentTypeError(
                "Port must be between 0 and 65535")
        return x

    parser = argparse.ArgumentParser()
    parser.add_argument('rules')
    parser.add_argument('host')
    parser.add_argument('port', type=ipv4_port_type)
    parser.add_argument('--verbose', '-v', action='count')
    return parser


def main():
    parser = _get_parser()
    args = parser.parse_args()
    logging.config.dictConfig(
        _logging_cfg(args.verbose)
    )

    twisted.internet.reactor.listenTCP(
        8000,
        twarf.proxy.TwarfFactory(
            args.rules, args.host, args.port
        )
    )
    try:
        print('Listening on port 8000')
        twisted.internet.reactor.run()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
