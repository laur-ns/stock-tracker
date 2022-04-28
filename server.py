from socket import *
import _thread
import json
import requests
import sys

API_KEY = "sk_b8783e173c464473b9e3a73239e32ba8"
serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = int(sys.argv[1])
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(("", serverPort))

serverSocket.listen(5)
print('The server is running')


# Server should be up and running and listening to the incoming connections

# Extract the given header value from the HTTP request message
def getHeader(message, header):
    if message.find(header) > -1:
        value = message.split(header)[1].split()[0]
    else:
        value = None

    return value


def getFile(filename):
    try:
        f = open(filename, "rb")

        body = f.read()
        if filename.endswith(".js"):
            header = (
                "HTTP/1.1 200 OK\r\nContent-Type: text/javascript\r\n\r\n").encode()
        elif filename.endswith(".json"):
            header = (
                "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n").encode()
        else:
            header = ("HTTP/1.1 200 OK\r\n\r\n")
    except IOError:
        # Send HTTP response message for resource not found
        header = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        body = "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode()

    return header, body


# returns 401 if wrong/no credentials given
def no_auth(message):
    header = "HTTP/1.1 401 Unauthorized\r\nWWW-Authenticate: Basic realm=\"Stock-159\"\r\n\r\n".encode()
    body = (
        "<html><head></head><body><h1>ERROR</h1></body></html>\r\n").encode()
    return header, body


# default service function
def default(message):
    header = "HTTP/1.1 200 OK\r\n\r\n".encode()
    body = (
        "<html><head></head><body><h1>WELCOME</h1></body></html>\r\n").encode()
    return header, body

# ---------- PORTFOLIO FUNCTIONS ----------

# updates gain/loss using api endpoint.


def update_gain_loss():
    with open("portfolio.json", "r") as file:
        data = json.load(file)
        for index, symbol in enumerate(data["Stocks"]):
            try:
                response = requests.get(
                    f"https://cloud.iexapis.com/stable/stock/{symbol['Name']}/quote?token={API_KEY}").json()
            except:
                # if it throws an error, it likely means the symbol doesn't exist, so delete it from json file
                # in reality the server might just be down and it would end up falsely deleting the stock
                print('[ERROR]: symbol not found, deleting symbol...')
                data["Stocks"].pop(index)
                continue
            latest_quote = response["latestPrice"]
            gain_or_loss = (
                latest_quote - symbol["Price"]) / symbol["Price"] * 100
            symbol["GainLoss"] = round(gain_or_loss, 2)
        json_data = json.dumps(data)
    with open("portfolio.json", "w") as file:
        file.write(json_data)


def validate_input(input):
    # validate input by testing if the name's a string
    # and if the quantity and price can both be converted
    # to the appropriate data types
    s = input.split("&")
    name = s[0].split("=")[1]
    if type(name) is not str:
        return False
    try:
        quantity = int(s[1].split("=")[1])
        price = float(s[2].split("=")[1])
    except:
        return False
    return True


def add_to_portfolio(input):
    # should only run if input is validated beforehand
    with open("portfolio.json", "r") as data:
        data = json.load(data)
        is_new_stock = True
        s = input.split("&")
        name = s[0].split("=")[1].upper()
        quantity = int(s[1].split("=")[1])
        price = float(s[2].split("=")[1])
        gain_loss = None

        # check if symbol already exists, if so, update/remove
        for index, symbol in enumerate(data["Stocks"]):
            if symbol["Name"] == name:  # can only reduce/remove
                is_new_stock = False
                if quantity < 0:  # turn it positive and subtract quantity
                    quantity *= -1
                symbol["Quantity"] -= quantity
            if symbol["Quantity"] == 0:
                data["Stocks"].pop(index)

        if is_new_stock is True:
            new_stock = {
                "Name": name,
                "Quantity": int(quantity),
                "Price": round(float(price), 2),
                "GainLoss": gain_loss
            }
            data["Stocks"].append(new_stock)

        json_data = json.dumps(data)
    with open("portfolio.json", "w") as outfile:
        outfile.write(json_data)


def portfolio(message):
    try:
        form_input = message.split()[-1]
        # if invalid input, do nothing with the input, continue updating gain/loss
        if "stocksymbol" in form_input and validate_input(form_input):
            add_to_portfolio(form_input)
        update_gain_loss()
        body = open("portfolio.html", "r").read().encode()
        header = ("HTTP/1.1 200 OK\r\n\r\n").encode()
    except IOError:
        # Send HTTP response message for resource not found
        header = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        body = "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode()
    return header, body
# ----------  ----------

# ---------- RESEARCH FUNCTIONS ----------


def research(message):
    try:
        body = open("research.html", "r").read().encode()
        header = ("HTTP/1.1 200 OK\r\n\r\n").encode()
    except IOError:
        # Send HTTP response message for resource not found
        header = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        body = "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode()
    return header, body


def get_stock_data(message):
    header = ("HTTP/1.1 200 OK\r\n\r\n").encode()
    form_input = message.split("/")[1]
    try:
        # take both stock data and chart data for the symbol searched
        # append both in a single list and return with each data in
        # their corresponding indices
        stock_data = []
        stock_data.append(requests.get(
            f"https://cloud.iexapis.com/stable/stock/{form_input}/stats?token={API_KEY}").json())
        chart_data = requests.get(
            f"https://cloud.iexapis.com/stable/stock/{form_input}/chart/5y?chartCloseOnly=true&token={API_KEY}").json()
        body = []
        body.append(stock_data)
        body.append(chart_data)
        body = json.dumps(body).encode()
    except:
        header = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        body = "<html><head></head><body><h1>Symbol does not exist</h1></body></html>\r\n".encode()
    return header, body


# ---------- ----------

def process(connectionSocket):
    # Receives the request message from the client
    message = connectionSocket.recv(1024).decode()

    if len(message) > 1:
        authenticated = False
        # compares basic encoded credentials with the one in string
        try:
            auth_header = message.split().index("Authorization:")
            credentials = message.split()[auth_header + 2]
            if credentials != "MjEwMTE4Nzc6MjEwMTE4Nzc=":  # username: 21011877, password: 21011877
                responseHeader, responseBody = no_auth(message)
            else:
                authenticated = True
        except:
            responseHeader, responseBody = no_auth(message)

        resource = message.split()[1][1:]
        # map requested resource (contained in the URL) to specific function which generates HTTP response
        if authenticated:
            if resource == "portfolio":
                responseHeader, responseBody = portfolio(message)
            elif resource == "research":
                responseHeader, responseBody = research(message)
            elif "research/" in resource:
                # get data from api endpoint and send back javascript
                responseHeader, responseBody = get_stock_data(resource)
            elif resource == "portfolio.js":
                responseHeader, responseBody = getFile(resource)
            elif resource == "stock-symbols.json":
                responseHeader, responseBody = getFile(resource)
            elif resource == "portfolio.json":
                responseHeader, responseBody = getFile(resource)
            else:
                responseHeader, responseBody = default(message)
    else:
        responseHeader, responseBody = default(message)

    # Send the HTTP response header line to the connection socket
    connectionSocket.send(responseHeader)
    # Send the content of the HTTP body (e.g. requested file) to the connection socket
    connectionSocket.send(responseBody)
    # Close the client connection socket
    connectionSocket.close()


# Main web server loop. It simply accepts TCP connections, and get the request processed in seperate threads.
while True:
    # Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()
    # Clients timeout after 60 seconds of inactivity and must reconnect.
    connectionSocket.settimeout(60)
    # start new thread to handle incoming request
    _thread.start_new_thread(process, (connectionSocket,))
