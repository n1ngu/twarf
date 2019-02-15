
import sys
import argparse
import logging.config

import twarf.app


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
    parser.add_argument('port', type=ipv4_port_type)
    parser.add_argument('--verbose', '-v', action='count')
    return parser


def main():
    parser = _get_parser()
    args = parser.parse_args()
    logging.config.dictConfig(
        _logging_cfg(args.verbose)
    )

    import twisted.internet.reactor
    app = twarf.app.Twarf(
        args,
        twisted.internet.reactor)
    try:
        app.run()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
