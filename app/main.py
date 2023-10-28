# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    conn, addr = server_socket.accept()  # wait for client

    response = "HTTP/1.1 200 OK\r\n\r\n"

    err_response = "HTTP/1.1 404 NOT FOUND\r\n\r\n"

    data = conn.recv(1024).decode("utf-8")
    path = data.split(" ")[1]

    if path == "/":
        conn.send(response.encode())

    elif path.startswith("/echo/"):
        content = path.split("/echo/")[1]
        content_length = len(content)

        res = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n {content}"
        conn.send(res.encode())

    else:
        conn.send(err_response.encode())


if __name__ == "__main__":
    main()
