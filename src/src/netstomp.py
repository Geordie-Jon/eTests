#! /usr/bin/python
'''
Created on 6 Dec 2015

@author: root
'''
import sys
import socket
import argparse
import threading
import enum
import logging

try:
    import subprocess32 as subprocess
except ImportError:
    print('non-unix system or subprocess32 not installed, using subprocess')
    import subprocess


class LogVerbosity(enum.Enum):
    debug = logging._levelNames
listen = False
command = False
upload = False
execute = ''
target = ''
upload_destination = ''
port = 0


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('target_host')
    parser.add_argument('port', type=int)
    parser.add_argument('-l', '--listen', action='store_true',
                        help='Listen on [host]:[port] for incoming connections')
    parser.add_argument('-c', '--command', default='', action='store_true',
                        help='initialise a command shell',
                        )
    parser.add_argument('-u', '--upload', default='', dest='upload_destination',
                        help='upon receiving a connection, upload a file and write to [destination]')
    parser.add_argument('-v', '--verbosity', action='count', default=0,
                        help='increase output verbosity')
    args = parser.parse_args()
    level = (xrange(60, -1, -10)[min(6, args.verbosity)])
    logging.basicConfig(level=level)
    logging.log(level + 1, 'ADMIN: {}'.format(args))
    logging.critical('level set')
    logging.fatal('level set')
    logging.error('level set')
    logging.warn('level set')
    logging.info('level set')
    logging.debug('level set')
    logging.log(1, '!Always log!')


if __name__ == '__main__':
    main(sys.argv[1:])
