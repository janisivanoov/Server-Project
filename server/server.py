import http.server
import socketserver
from eth_typing.evm import HexAddress
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
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import Base
from typing import List
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from uint import Uint, Int
from pydantic import BaseModel
from sqlalchemy.orm import relationship
import threading
import time
# DATABASE PART

# Contract address
contract_address = "0xa274d4daaff01e3aa710907aabdd57d036c96cec"
w3 = web3.Web3(web3.IPCProvider("/home/node/geth.ipc"))

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

#WS method

IFilter = w3.eth.filter(
    {
        "topics": [[
            #sync
            "0x1c411e9a96e071241c2f21f7726b17ae89e3cab4c78be50e062b03a9fffbbad1",
            #swap
            "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822"
            ]]        
    }
)

def IFilter_Logging(IFilter, poll_interval):
    while True:
        #output to database
        print(IFilter.get_new_entries())
        time.sleep(poll_interval)

T = threading.Thread(target = IFilter_Logging, args = (IFilter,1))
T.start()
T.join()

#HTTP method











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



# FastAPI 


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Pair(Base):
    pair = "pair"


    reserve0 = Column(Integer, primary_key=True, index=True)
    reserve1 = Column(Integer, primary_key=True, index=True)
    token0 = Column(Integer, primary_key=True, index=True)
    token1 = Column(Integer, primary_key=True, index=True)
    fee = Column(Integer, primary_key=True, index=True)
    address = Column(Integer, primary_key=True, index=True)

class PairBase(BaseModel):
    reserve0: Uint
    reserve1: Uint
    token0: hex(20)
    token1: hex(20)
    fee: Uint
    address: hex(20)


class PairCreate(PairBase):
    pass


class Pair(PairBase):
    reserve0: Uint
    reserve1: Uint
    token0: hex(20)
    token1: hex(20)
    fee: Uint
    address: hex(20)

    class Config:
        orm_mode = True