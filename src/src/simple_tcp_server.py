'''
Created on 6 Dec 2015

@author: root
'''
import socket
import threading

bind_ip = '0.0.0.0'
bind_port = 9999
address = bind_ip, bind_port

server = socket.socket(socket.AF_INET,  # IPv4
                       socket.SOCK_STREAM
                       )
server.bind(address)
server.listen(5)

print('[*] Listening on {}:{:04d}'.format(
    *address))

# handle thread


def handle_client(client_socket):
    request = client_socket.recv(1024)
    print('[+] Received: {}'.format(request))
    client_socket.send('ack!')
    client_socket.close()

while True:
    client, address = server.accept()
    print("[*] Accepted connection from {}:{:04d}".format(*address))
    client_handler = threading.Thread(
        target=handle_client, args=(client,))
    print('[*] Starting thread {}'.format(client_handler.name))
    client_handler.start()
server.close()
