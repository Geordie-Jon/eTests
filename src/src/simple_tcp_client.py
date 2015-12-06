'''
Created on 6 Dec 2015

@author: root
'''
import socket

target_host = '127.0.0.1'  # 'www.google.com'
target_port = 9999  # 80

client = socket.socket(socket.AF_INET,  # IPv4
                       socket.SOCK_STREAM  # client
                       )

client.connect((target_host, target_port))
client.send("ABCDEF")

response = client.recv(4096)
print(response)
