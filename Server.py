import socket
import Request_Handler
import Response_Handler

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(('127.0.0.1', 80))


def send_msg(client_socket, msg, is_img):
    """
    Summary
    -------
        sends the message
    Parameters
    ----------
        client_socket : socket.pyi
            the socket of the client
        msg : str/bytes
            the headers and the content needed to be sent
        is_img : bool
            true if the message is an img
    """
    if is_img:
        client_socket.send(msg)
    else:
        client_socket.send(msg.encode())
    print("Sent")
    print()


def main():
    """
    Summary
    -------
        the main function responsible for keeping the server up, running and ready for requests
    Parameters
    ----------

    """
    while True:
        ss.listen()
        print("running")
        print()

        (client_socket, address) = ss.accept()
        print("Connected Bitch On" + str(address))
        print()

        req_d = Request_Handler.receive(client_socket)
        if req_d:
            valid_req = Request_Handler.check_req(req_d)
            message = Response_Handler.create_response(req_d, valid_req)
            if message:
                # print(message)
                send_msg(client_socket, message[0], message[1])


if __name__ == "__main__":
    main()
