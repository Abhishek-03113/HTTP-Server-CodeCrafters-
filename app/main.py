# Uncomment this to pass the first stage
import socket
from typing import Required


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

        res = (
            "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
            f"Content-Length: {content_length}\r\n\r\n"
            f"{content}"
        )
        conn.send(res.encode())
    elif path == "/user-agent":
        usrAgent = data.split("\r\n")
        user_agent = str()

        for agent in usrAgent:
            if agent.startswith("User-Agent"):
                user_agent = agent.split("User-Agent:")[1].strip()

        content_length = len(user_agent)
        content = user_agent

        userAgentRes = (
            "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
            f"Content-Length: {content_length}\r\n\r\n"
            f"{content}"
        )

        conn.send(userAgentRes.encode())

    else:
        conn.send(err_response.encode())


if __name__ == "__main__":
    main()
