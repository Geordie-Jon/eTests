#! /usr/bin/python
'''
netstomp.py
Teaching cats about networking.
Created on 6 Dec 2015

@author: root
'''
from __future__ import print_function
import sys
import socket
import argparse
import threading
import logging

try:
    import subprocess32 as sp
except ImportError:
    print('non-unix system or subprocess32 not installed, using subprocess')
    import subprocess as sp


def client_sender(buffr):
    global args
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((args.target, args.port))
        if buffr:
            client.send(buffr)
        while True:
            recv_len = 1
            response = ''
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data
                if recv_len < 4096:
                    break
            print(response)
            buffr = raw_input('')
            buffr += '\n'
            client.send(buffr)
    except Exception as e:
        logging.fatal(repr(e))
        # raise
    except:
        print('classic')
    finally:
        client.close()


def server_loop():
    global args
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM)
    target = (args.target if args.target else '0.0.0.0')
    server.bind((target, args.port))
    server.listen(5)
    try:
        while True:
            client_socket, _ = server.accept()
            client_thread = threading.Thread(target=client_handler,
                                             args=(client_socket,))
            client_thread.start()
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        server.close()


def run_command(command):
    command = command.rstrip()
    try:
        output = sp.check_output(command,
                                 stderr=sp.STDOUT,
                                 shell=True)
    except Exception as e:
        output = 'Failed to execute command - "{!s}"'.format(e)
    except:
        output = 'Failed to execute command - "classic"'
    return output


def client_handler(client_socket):
    global args
    if args.upload_destination:
        file_buffer = ''
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data
        try:
            with open(args.upload_destination, 'wb') as file_descriptor:
                file_descriptor.write(file_buffer)
        except Exception as e:
            client_socket.send(
                'Failed to save file to {}\n{!s}\r\n'.format(
                    args.upload_destination, e))
        else:
            client_socket.send(
                'Successfully saved file to {}\r\n'.format(
                    args.upload_destination))
    if args.execute:
        output = run_command(args.execute)
        client_socket.send(output)
    if args.command:
        while True:
            client_socket.send('ENTER A COMMAND:> ')
            cmd_buffer = ''
            while '\n' not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
            response = run_command(cmd_buffer)
            client_socket.send(response)


def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', default='')
    parser.add_argument('-p', '--port', type=int)
    parser.add_argument(
        '-l', '--listen', action='store_true',
        help='Listen on [host]:[port] for incoming connections')
    parser.add_argument(
        '-e', '--execute', default='',
        help='execute the given file upon receiving a connection')
    parser.add_argument('-c', '--command', default='', action='store_true',
                        help='initialise a command shell',
                        )
    parser.add_argument(
        '-u', '--upload', default='', dest='upload_destination',
        help='upon receiving a connection, upload a file and write to\
        [destination]')
    parser.add_argument('-v', '--verbosity', action='count', default=0,
                        help='increase output verbosity')
    args = parser.parse_args()
    level = (xrange(60, -1, -10)[min(6, args.verbosity)])
    logging.basicConfig(level=level)
    if not level:
        logging.log(level + 1, 'ADMIN: {}'.format(args))
        logging.critical('level set')
        logging.fatal('level set')
        logging.error('level set')
        logging.warn('level set')
        logging.info('level set')
        logging.debug('level set')
        logging.log(1, '!Always log!')
    if not args.listen and args.target and args.port:
        try:
            buffr = sys.stdin.read()
        except (KeyboardInterrupt, EOFError):
            logging.debug('[-] skipped command read')
        else:
            try:
                client_sender(buffr)
            except Exception as e:
                return str(e)
    if args.listen:
        server_loop()

    return 'Hello World'

if __name__ == '__main__':
    #     print('{!StompNet*' * 50, file=sys.stdout, end='\r\n')
    sys.exit(main())
