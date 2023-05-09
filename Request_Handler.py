import Variables
import os


def receive(client_socket):
    """
    Summary
    -------
        receives the headers of the request
    Parameters
    ----------
        client_socket : socket.pyi
            the socket of the client
    """
    request = ""
    while True:
        request += client_socket.recv(1).decode()
        if "\r\n\r\n" in request:
            break
    print(request)
    reqest_s = request.split("\r\n")
    d = {reqest_s[0]: None}
    for header in reqest_s[1:-2:]:
        header = header.split(":")
        d[header[0]] = header[1]
    d["End"] = request[-4:]
    if "Content-Length" in d:
        receive_content(client_socket, d)
        client_socket.send("Uploaded".encode())
        return None
    return d


def receive_content(client_socket, d):
    """
    Summary
    -------
        receives the content if content was sent
    Parameters
    ----------
        client_socket : socket.pyi
            the socket of the client
        d : dict
            dictionary of request Headers
    """
    url = [*d.keys()][0].split()[1]
    file_path = url.split("?")[0][1:] + "s/"
    file_name = url.split("=")[-1]

    with open(file_path + file_name, "wb") as f1:
        resp = client_socket.recv(int(d["Content-Length"]))
        f1.write(resp)


def check_req(req_d):
    """
    Summary
    -------
        checks the headers of the request
    Parameters
    ----------
         req_d : dict
            dictionary of request Headers
    """
    keys = [*req_d]
    link = "Networks/4.4/" + keys[0].split(" ")[1][1:]
    if "image?image-name=" in link:
        url = [*req_d.keys()][0].split()[1]
        file_name = url.split("=")[-1]
        link = "Networks/4.4/webroot/" + file_name
    if Variables.function_request[0] not in keys[0] or Variables.function_request[1] not in keys[0]:
        if not os.path.exists(link):
            return False
    if not req_d["Host"] != '127.0.0.1':
        return False
    if not req_d["End"] == "\r\n\r\n":
        return False
    return True
