import os
import Variables
from magic import from_file


def get_img():
    """
    Summary
    -------
        reads the img and returns its content
    Parameters
    ----------

    """
    with open("Networks/4.4/" + file_path, "rb") as f1:
        f1_con = f1.read()
    return f1_con


def get_text():
    """
    Summary
    -------
        reads the text file and returns its content
    Parameters
    ----------

    """
    with open(file_path, "r", encoding="utf-8") as f1:
        f1_con = f1.read()
    return f1_con


def find_type():
    """
    Summary
    -------
        using magic module identifies the file types by checking its file name extensions
    Parameters
    ----------

    """
    try:
        if file_path[-(file_path[::-1].find(".")):] == "css":
            return "text/css"
        typ = str(from_file(file_path, mime=True))
        return typ
    except:
        return "not supported type"


def calculate_next():
    """
    Summary
    -------
        extracts the inputted character, calculates and returns the correct response
    Parameters
    ----------

    """
    text = file_path.split("=")
    text = text[-1]
    try:
        text = str(int(text) + 1)
    except:
        text = "YOU FUCK!!!! this is unacceptable you will not be forgiven for that. have a great day."
    return text


def calculate_area():
    """
    Summary
    -------
        extracts the inputted characters, calculates and returns the correct response
    Parameters
    ----------

    """
    text = file_path.split("?")[1]
    text = text.split("&")
    width = text[0].split("=")[-1]
    height = text[1].split("=")[-1]
    try:
        s_area = str((int(width) * int(height)) / 2)
    except:
        s_area = "YOU FUCK!!!!! this is unacceptable you will not be forgiven for that. have a great day."
    return s_area


def create_response(req_d, valid_req):
    """
    Summary
    -------
        using the request from the client it determines the correct response creates it and returns it
    Parameters
    ----------
        req_d : dict
            dictionary of request Headers
        valid_req : bool
            true if request is valid

    """
    global file_path
    img = False
    file_path = [*req_d][0].split()[1][1:]
    if "image?image-name=" in file_path:
        file_path = file_path.split("image?image-name=")
        file_path = "webroot/uploads/" + file_path[1]
    text = ""
    the_type = find_type()
    typ_of_func = file_path.split("/")[-1].split("?")[0]
    if typ_of_func in Variables.function_request:
        typ_of_func = typ_of_func.replace("-", "_")
        text = eval(typ_of_func)()
        the_type = "text/plain"

    else:
        if not not os.path.exists(file_path):
            headers = "HTTP/1.1 404 Not Found" + "\r\n"
            if file_path[-4:] == "html":
                file_path = "webroot/404 NF.html"
                headers += "\r\n" + get_text()
            return headers, img

    if the_type != "not supported type":
        if the_type.split("/")[0] == "text":
            text = get_text()
        if the_type.split("/")[0] == "image":
            text = get_img()
            img = True
        headers = "HTTP/1.1 200 OK " + "\r\n"
        headers += "Content-Length: " + str(len(text)) + "\r\n"
        headers += "Content-Type: " + str(the_type) + "\r\n"
    else:
        headers = "HTTP/1.1 404 Not Found" + "\r\n"
    headers += "\r\n"

    if img:
        headers = headers.encode()
    headers += text

    return headers, img
