#!/usr/bin/env python3

'''
Dgram Unix Socket test program
'''

import socket
import sys
import argparse

def getargs():
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('socket_path', metavar='socket-path', help='path to socket file')
	parser.add_argument('--buffer-size', type=int, default=1024, help='the buffer size (max packet size)')
	subparsers = parser.add_subparsers(help='only you can choose: send or receive??')

	receive_parser = subparsers.add_parser('recv', help='run in receive mode')
	receive_parser.set_defaults(func=main_receive)

	send_parser = subparsers.add_parser('send', help='run in send mode')
	send_parser.add_argument('messages', nargs='*', type=str, default=['hello'], help='the message(s) to send')
	send_parser.set_defaults(func=main_send)

	return parser.parse_args()

def main(args):
	with socket.socket(family=socket.AF_UNIX, type=socket.SOCK_DGRAM) as sock:
		args.func(args, sock)

def main_receive(args, sock):
	sock.bind(args.socket_path)

	while True:
		print(sock.recv(args.buffer_size).decode('utf-8'))

def main_send(args, sock):
	sock.connect(args.socket_path)
	
	for message in args.messages:
		if len(message) > args.buffer_size:
			logger.warn('message size ({:d}) exceeds buffer length ({:d})'.format(len(message), args.buffer_size))
		sock.send(message.encode('utf-8'))

if __name__=='__main__':
	try:
		main(getargs())
	except KeyboardInterrupt:
		print('exiting gracefully', file=sys.stderr)
