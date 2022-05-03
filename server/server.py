import http.server
import socketserver
import mysql.connector
from mysql.connector import errorcode
import sys
import cgi
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from logging import error, exception
import urllib.request
import web3
from web3.auto import w3
from web3 import Web3 
import json
from web3 import Web3
import asyncio

# DATABASE PART

#contract_address = "0xa274d4daaff01e3aa710907aabdd57d036c96cec"
#cont_addr = int(("address")(contract_address))

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

# Initialise WEB3 ENS
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/e1aff836d3a64d6aba0f028217da381f"))

import mysql.connector
from mysql.connector import errorcode

eth_key = "7I39Q4ZZ6SER7ZZTKQMNGYHD3UTZ6BSQ32"
eth_contract = "0xa274d4daaff01e3aa710907aabdd57d036c96cec"

maxcount = 100

rrabi = [
  {
    "inputs": [
      {
        "internalType": "uint112",
        "name": "reserve0",
        "type": "uint112"
      },
      {
        "internalType": "uint112",
        "name": "reserve1",
        "type": "uint112"
      }
    ],
    "name": "Sync",
    "outputs": [
      {
        "internalType": "uint112",
        "name": "reserve0",
        "type": "uint112"
      },
      {
          "internalType": "uint112",
          "name": "reserve1",
          "type": "uint112"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]

rrcontract = w3.eth.contract(address = Web3.toChecksumAddress('0xa274d4daaff01e3aa710907aabdd57d036c96cec'), abi = rrabi)


# Function Reads First block    

def getBlock():
    # read block number
    q_block = "SELECT Max(block) from server.test_info"
    cursor.execute(q_block)
    for (block) in cursor:
        start_block = block
    if start_block == (None,):
        start_block = (0,)
    return start_block[0]


# Function updates reverse registry table
def updateName(domain, address, block):
    i_name = "insert into test_info (addr, name, block) values (%s, %s, %s)"
    u_name = "update test_info set name = %s, block=%s where addr = %s"
    d_name = "delete from test_info where addr = %s"
    if domain != "":
        if domain == "None":
            # delete name from the registry
            cursor.execute(d_name, [address])
            my_cn.commit()
        else:
            # insert or update
        
            try:
                # attempt to insert
                cursor.execute(i_name, [address, domain, block])
            except mysql.connector.Error as err:
                # update if record is there
                if err.errno == 1062:
                    cursor.execute(u_name, [domain, block, address])
                else:
                    print (err)
                    quit()
            finally:
                my_cn.commit()

#TEST-----------------------------------------------------------------------------------------------------------------------------------------------------------

#event_signature_hash = Web3.keccak(text="Sync(uint32)").hex()
#event_filter = w3.eth.filter({
   # "address": cont_addr,
   # "topics": [event_signature_hash,
   #            "0x1c411e9a96e071241c2f21f7726b17ae89e3cab4c78be50e062b03a9fffbbad1"],
   # })

# Close the cursor and the connection
cursor.close()
my_cn.close()

















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
