# Uncomment this to pass the first stage
import socket
from typing import Required
import threading
import sys
import os 
import argparse


HTTP_OK = "HTTP/1.1 200 OK\r\n"
HTTP_NOT_FOUND = "HTTP/1.1 404 Not Found\r\n"

def handleClient(client,args):



    request = client.recv(4096)

    type_of_request = request.decode().split(" ")[0]
    path = request.decode().split(" ")[1]
    content = path[6:]
    if type_of_request == "POST" and path.startswith("/files/"):
        filename = path[7:]
        directory = args.directory
        filepath = os.path.join(directory, filename)
        with open(filepath, "w") as f:
            content_to_r = request.decode().split("\r\n\r\n")[1]
            f.write(content_to_r)
            res = f"HTTP/1.1 201 Created\r\nContent-Type: text/plain\r\nContent-Length: {len(content_to_r)}\r\n\r\n{content_to_r}"

            client.send(res.encode())

    request = request.decode().splitlines()


    response = get_response(request)

    # path = get_path_from_request(request)

    # if path == "/":
    #     response = (
    #         "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n"
    #     )
    # elif path == "/user-agent":
    #     user_agent = get_user_agent_from_request(request)
    #     response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}"
    # elif path.startswith("/echo/"):
    #     random_string = path[6:]  # Extract the random string from the path
    #     response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {}\r\n\r\n{}".format(
    #         len(random_string), random_string
    #     )
    # else:
    #     # Respond with 404 Not Found for paths that do not match "/echo/" or "/user-agent"
    #     response = "HTTP/1.1 404 Not Found\r\n\r\n"

    client.send(response.encode())  # Encode the string to bytes
    # Close the connection
    client.close()

#get Response 

def get_response(request, files=None):
    _, path, _ = request[0].split(" ")
    if path == "/":
        response = HTTP_OK + "\r\n"
    elif path.startswith("/echo"):
        content = path.split("/echo/")[1]
        response = (
            HTTP_OK + "Content-Type: text/plain\r\n"
            f"Content-Length: {len(content)}\r\n"
            "\r\n"
            f"{content}\r\n"
        )
    elif path.startswith("/user-agent"):
        content = request[2].split(": ")[1]
        response = (
            HTTP_OK + "Content-Type: text/plain\r\n"
            f"Content-Length: {len(content)}\r\n"
            "\r\n"
            f"{content}\r\n"
        )
    elif path.startswith("/files"):
        file_name = path.split("/files/")[1]
        file_content = handle_files(file_name)
        if file_content:
            response = (
                HTTP_OK + "Content-Type: application/octet-stream\r\n"
                f"Content-Length: {len(file_content)}\r\n"
                "\r\n"
                f"{file_content}\r\n"
            )
        else:
            response = HTTP_NOT_FOUND + "\r\n"
    else:
        response = HTTP_NOT_FOUND + "\r\n"
    
    return response

# function to handle files 
def handle_files(file_name):
    try:
        with open(f"{FILES_DIR}{file_name}", "r") as f:
            file = f.read()
    except FileNotFoundError:
        file = None
    return file


# get path from the request 

# def get_path_from_request(request):
#     # Split the request into lines and extract the path from the first line
#     lines = request.split("\r\n")
#     if lines:
#         # The first line should look like "GET /echo/abc HTTP/1.1"
#         parts = lines[0].split(" ")
#         if len(parts) > 1:
#             return parts[1]
#     # If the path cannot be extracted, return a default value
#     return "/"


# Get user agent 
# def get_user_agent_from_request(request):
#     # Split the request into lines and find the User-Agent header
#     lines = request.split("\r\n")
#     for line in lines:
#         if line.startswith("User-Agent:"):
#             return line.split("User-Agent:")[1].strip()
#     # If the User-Agent header is not found, return a default value
#     return "Unknown User Agent"

def main(args):
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    if args:
        global FILES_DIR
        FILES_DIR = args[1]
    


    while True:
        client, addr = server_socket.accept()  # wait for client

        parser = argparse.ArgumentParser()
        parser.add_argument("--directory", default="")
        args = parser.parse_args()
        print(f"the args: {args}")

        client_thread = threading.Thread(target=handleClient,args=(client,args))

        client_thread.start()


    # data = conn.recv(1024).decode("utf-8")

   

    # if path == "/":
    #     conn.send(response.encode())

    # elif path.startswith("/echo/"):
    #     content = path.split("/echo/")[1]
    #     content_length = len(content)

    #     res = (
    #         "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
    #         f"Content-Length: {content_length}\r\n\r\n"
    #         f"{content}"
    #     )
    #     conn.send(res.encode())
    # elif path == "/user-agent":
    #     usrAgent = data.split("\r\n")
    #     user_agent = str()

    #     for agent in usrAgent:
    #         if agent.startswith("User-Agent"):
    #             user_agent = agent.split("User-Agent:")[1].strip()

    #     content_length = len(user_agent)
    #     content = user_agent

    #     userAgentRes = (
    #         "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
    #         f"Content-Length: {content_length}\r\n\r\n"
    #         f"{content}"
    #     )

    #     conn.send(userAgentRes.encode())

    # else:
    #     conn.send(err_response.encode())

    
if __name__ == "__main__":
    main(sys.argv[1:])

