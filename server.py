import socket
import os
import sys

def send_all(sock, data):
    total_sent = 0
    if isinstance(data, str):
        data = data.encode()

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
    raw_length = recv_exact(sock, 10)
    if not raw_length:
        return None
    msg_length = int.from_bytes(raw_length, byteorder='big')
    msg = recv_exact(sock, msg_length)
    return msg.decode()



def handle_ls(ctrl_sock, data_port, client_addr):
    data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_sock.connect((client_addr[0], data_port))
    listings = os.listdir('.')
    send_msg(data_sock, '\n'.join(listings))
    data_sock.close()
    send_msg(ctrl_sock, "completed")



def handle_get(ctrl_sock, filename, data_port, client_addr):
    if not os.path.isfile(filename):
        send_msg(ctrl_sock, f"error: '{filename}' not found")
        return

    data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_sock.connect((client_addr[0], data_port))
    with open(filename, 'rb') as f:
        file_data = f.read()
    send_msg(data_sock, file_data)
    data_sock.close()
    send_msg(ctrl_sock, "completed")

def handle_put(ctrl_sock, filename, data_port, client_addr):
    data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_sock.connect((client_addr[0], data_port))
    file_data = recv_msg(data_sock)
    with open(filename, 'wb') as f:
        f.write(file_data.encode())
    data_sock.close()
    send_msg(ctrl_sock, "completed")



def main():
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    ctrl_port = int(sys.argv[1])
    ctrl_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ctrl_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ctrl_sock.bind(('', ctrl_port))
    ctrl_sock.listen(5)
    print(f"Server listening on port {ctrl_port}...")

    while True:
        ctrl, (client_ip, client_port) = ctrl_sock.accept()
        print(f"Accepted connection from {client_ip}:{client_port}")
        if not msg(ctrl):
            break
        parts = msg(ctrl).split()
        cmd = parts[0].upper()

        if cmd == "QUIT":
            send_msg(ctrl, "Goodbye!")
            ctrl.close()
            break
        elif cmd == "LS":
            data_port = int(parts[1])
            handle_ls(ctrl, data_port, (client_ip, client_port))
        elif cmd == "GET":
            filename = parts[1]
            data_port = int(parts[2])
            handle_get(ctrl, filename, data_port, (client_ip, client_port))
        elif cmd == "PUT":
            filename = parts[1]
            data_port = int(parts[2])
            handle_put(ctrl, filename, data_port, (client_ip, client_port))
        else:
            send_msg(ctrl, f"error: unknown command '{cmd}'")

            ctrl.close()
            print(f"Closed connection from {client_ip}:{client_port}")


if __name__ == "__main__":
    main()