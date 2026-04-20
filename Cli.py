import socket
import os
import sys

def send_all(sock, data):
    if isinstance(data, str):
        data = data.encode()
    total_sent = 0
    while total_sent < len(data):
        sent = sock.send(data[total_sent:])
        if sent == 0:
            raise RuntimeError("Socket connection broken")
        total_sent += sent

def recv_exact(sock, n):
    data = b''
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise RuntimeError("Socket connection broken")
        data += chunk
    return data

def send_msg(sock, msg):
    if isinstance(msg, str):
        msg = msg.encode()
    send_all(sock, msg)

def recv_msg(sock):
    header = recv_exact(sock, 10)
    if not header:
        return None
    msg_length = int(header.decode().strip())
    msg = recv_exact(sock, msg_length)
    return msg.decode()

def get_ephemeral_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    sock.listen(1)
    port = sock.getsockname()[1]
    sock.close()
    return port

def do_ls(ctrl_sock):
    data_port = get_ephemeral_port()
    data_srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    data_srv.bind(('localhost', data_port))
    data_srv.listen(1)
    send_msg(ctrl_sock, f"data_port {data_port}")
    data_sock, _ = data_srv.accept()
    data_srv.close()
    print(recv_msg(ctrl_sock))
    data_sock.close()
    print(recv_msg(ctrl_sock))

def do_get(ctrl_sock, filename):

def do_put(ctrl_sock, filename):

def main():

