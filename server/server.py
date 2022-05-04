import http.server
import socketserver
import mysql.connector
from mysql.connector import errorcode
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from logging import error, exception
import urllib.request
import web3
from web3.auto import w3
from web3 import Web3 
import json
from web3 import Web3
import json
from web3 import Web3
import asyncio
import mysql.connector
from mysql.connector import errorcode
from web3 import Web3
import json
import time

# DATABASE PART

# Contract address
contract_address = "0xa274d4daaff01e3aa710907aabdd57d036c96cec"

# Initializing parameters
my_config = {
  'user': 'server_user',
  'password': 'password1224!',
  'host': 'localhost',
  'database': 'server',
  'raise_on_warnings': True
}

# initializing MySQL connection
try:
  my_cn = mysql.connector.connect(**my_config)
except mysql.connector.Error as err:
    print(err)
    quit()
else:
  print ("Connected to the Database")
  
cursor =  my_cn.cursor() 

eth_key = "7I39Q4ZZ6SER7ZZTKQMNGYHD3UTZ6BSQ32"
eth_contract = "0xa274d4daaff01e3aa710907aabdd57d036c96cec"

infuraURL = "https://mainnet.infura.io/v3/e1aff836d3a64d6aba0f028217da381f"
account = "0xc623cAA847a077029624dEc1374a8f8C4d25035d"
contractAddress = "0x7b9fC3fBE0a4ff099126FcAdA64e70dEc6B4b07B"


web3 = Web3(Web3.HTTPProvider(infuraURL))


f = open('./ABI/EmitEvent.json')
abi = json.load(f)

# contract instance
EmitEvent = web3.eth.contract(address=contractAddress, abi=abi)

# filter for contract address
block_filter = web3.eth.filter({'fromBlock':'latest', 'address':contractAddress})


balance = web3.eth.getBalance(account)


# event object
newString_Event = EmitEvent.events.NewString()
newNumber_Event = EmitEvent.events.NewNumber()

def handle_event(event):
    
    receipt = web3.eth.waitForTransactionReceipt(event['transactionHash'])
    result = newString_Event.processReceipt(receipt)
    # print(result[0]['args']) 
    print(receipt)
    
def event_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
            time.sleep(poll_interval)

print("listening for events...")
event_loop(block_filter, 2)

















# SERVER PART

PORT = 8080 #localhost:8080
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()


class PythonServer(SimpleHTTPRequestHandler):

    def do_GET(self):
        iii = 0
        #TODO

    def do_POST(self):
        iii = 0
        #TODO

HOST_NAME = "localhost"
PORT = 8080

if __name__ == "__main__":
    server = HTTPServer((HOST_NAME, PORT), PythonServer)
    print(f"Server started http://localhost:8080")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Server stopped successfully")
        sys.exit(0)
