'''
Created on 6 Dec 2015

@author: root
'''
import socket

target_host = '127.0.0.1'
target_port = 9999

client = socket.socket(socket.AF_INET,  # IPv4
                       socket.SOCK_DGRAM  # client
                       )

client.sendto("AAABBBCCC",
              (target_host, target_port))

data, addr = client.recvfrom(4096)
print(data)
