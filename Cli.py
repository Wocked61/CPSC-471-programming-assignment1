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
    header = f"{len(msg):<10}".encode()
    send_all(sock, header + msg)

def recv_msg(sock):
    header = recv_exact(sock, 10)
    if not header:
        return None
    msg_length = int(header.decode().strip())
    msg = recv_exact(sock, msg_length)
    return msg.decode()

def get_ephemeral_port():
    tmp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tmp.bind(('localhost', 0))
    port = tmp.getsockname()[1]
    tmp.close()
    return port

def do_ls(ctrl_sock):
    data_port = get_ephemeral_port()
    data_srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    data_srv.bind(('localhost', data_port))
    data_srv.listen(1)
    print(f"sending ls command")
    send_msg(ctrl_sock, f"ls {data_port}")
    print(f"waiting for connection on port {data_port}")
    data_sock, _ = data_srv.accept()
    data_srv.close()
    print(f"sent ls command")
    print(recv_msg(data_sock))
    data_sock.close()
    print(recv_msg(ctrl_sock))

def do_get(ctrl_sock, filename):
    data_port = get_ephemeral_port()
    data_srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    data_srv.bind(('localhost', data_port))
    data_srv.listen(1)
    send_msg(ctrl_sock, f"get {filename} {data_port}")
    data_sock, _ = data_srv.accept()
    data_srv.close()
    file_content = recv_msg(data_sock)
    if file_content.startswith("ERROR"):
        print(file_content)
    else:
        print(f"{filename}, {len(file_content)} bytes transferred")
        with open(filename, 'w') as f:
            f.write(file_content)
    data_sock.close()
    recv_msg(ctrl_sock)

def do_put(ctrl_sock, filename):
    data_port = get_ephemeral_port()
    data_srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    data_srv.bind(('localhost', data_port))
    data_srv.listen(1)
    send_msg(ctrl_sock, f"put {filename} {data_port}")
    data_sock, _ = data_srv.accept()
    data_srv.close()
    with open(filename, 'r') as f:
        file_content = f.read()
    send_msg(data_sock, file_content)
    print(f"{filename}, {len(file_content)} bytes transferred")
    data_sock.close()

def main():
    if len(sys.argv) != 3:
        print("Usage: python Cli.py <server_ip> <server_port>")
        return
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    ctrl_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ctrl_sock.connect((server_ip, server_port))
    while True:
        cmd = input("ftp> ")
        if cmd == "ls":
            do_ls(ctrl_sock)
        elif cmd.startswith("get "):
            _, filename = cmd.split(maxsplit=1)
            do_get(ctrl_sock, filename)
        elif cmd.startswith("put "):
            _, filename = cmd.split(maxsplit=1)
            do_put(ctrl_sock, filename)
        elif cmd == "quit":
            send_msg(ctrl_sock, "quit")
            break
        else:
            print("Unknown command.")
    ctrl_sock.close()

if __name__ == "__main__":
    main()