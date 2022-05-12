#imports
import http.server
import socketserver
import urllib.request
from mysql.connector import cursor_cext
import web3
import json
import asyncio
import time
import threading
import sys
import mysql.connector

#from
from eth_typing.evm import HexAddress
from mysql.connector import errorcode
from http.server import HTTPServer, SimpleHTTPRequestHandler
from logging import error, exception
from web3.auto import w3
from web3 import Web3
from mysql.connector import errorcode
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from . import crud, models, schemas
from .database import Base, SessionLocal, engine
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request, Response, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.orm import relationship , Session
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)



# DATABASE(WS m.) PART



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
  
cursor0 =  my_cn.cursor() 

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




# SERVER PART(FastAPI)



# FastAPI 

app = FastAPI()

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/pairs/", response_model=schemas.Pair)
def create_user(pair: schemas.UPairCreate, db: Session = Depends(get_db)):
    db_pair = crud.get_pair_by_pairid(db, pair_id=pair.pair_id)
    if db_pair:
        raise HTTPException(status_code=400, detail="Pair already registered")

    #HTTP method

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
        "type": "event"
      },
      {
          "inputs": [
              {
                "internalType": "address",
                "name": "sender",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "reserve1",
                "type": "amount0In"
              },
              {
                  "internalType": "uint256",
                  "name": "amount1In",
                  "type": "uint256"
              },
              {
                  "internalType": "uint256",
                  "name": "amount0Out",
                  "type": "uint256"
              },
              {
                  "internalType": "uint256",
                  "name": "amount1Out",
                  "type": "uint256"
              },
              {
                  "internalType": "address",
                  "name": "to",
                  "type": "address"
              }
            ],
            "name": "Swap",
            "outputs": [
              {
                "internalType": "uint256",
                "name": "amount0In",
                "type": "uint256"
              },
              {
                  "internalType": "uint256",
                  "name": "amount1In",
                  "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "amount0Out",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "amount1Out",
                "type": "uint256"
              }
            ],
            "stateMutability": "view",
            "type": "event"
      }
    ]

    rrcontract = w3.eth.contract(address = Web3.toChecksumAddress(eth_contract), abi = rrabi)


    # Function Reads First block    
    
    #TODO: Change logic!!!
    #TODO: Change logic!!!
    #TODO: Change logic!!!
    #TODO: Change logic!!!

    # Function updates reverse registry table
    def updatePair(pair, address, block):
        i_pair = "insert into test_info (addr, name, block) values (%s, %s, %s)"
        u_pair = "update test_info set name = %s, block=%s where addr = %s"
        d_pair = "delete from test_info where addr = %s"
        if pair != "":
            if pair == "None":
                # delete
                cursor.execute(d_pair, [address])
                my_cn.commit()
            else:
                # insert or update

                try:
                    # attempt to insert
                    cursor.execute(i_pair, [address, pair, block])
                except mysql.connector.Error as err:
                    # update if record is there
                    if err.errno == 1062:
                        cursor.execute(u_pair, [pair, block, address])
                    else:
                        print (err)
                        quit()
                finally:
                    my_cn.commit()

    # Read topics into array

    topics = []
    c_sql = "select topic from ttopics"
    cursor0.execute(c_sql)
    for c in cursor0:
        topics.append(c)


    aaa = []
    bbb = []
    ccc = []
    b=0
    
    # loop with maxcount step

    while (b+maxcount<len(aaa)):
        addresses = aaa[b:b+maxcount]
        blocks = bbb[b:b+maxcount]
        topics = ccc[b:b+maxcount]

        try:
                pairs = rrcontract.functions.Swap(addresses).call()
                ii = 0
                for p in pairs:
                    print(addresses[ii] + "---" + p)
                    updatePair(str(p), str(addresses[ii]), str(topics[ii]), str(blocks[ii]))
                    ii += 1
        except BaseException as err:
                print("Exception. " + str(err))
        b += maxcount

        addresses = aaa[b:len(aaa)-1]
        blocks = bbb[b:len(bbb)-1]
        topics = ccc[b:len(ccc)-1]
        try:
            pairs = rrcontract.functions.Swap(addresses).call()
            ii = 0
            for p in pairs:
                print(addresses[ii] + "---" + p)
                updatePair(str(p), str(addresses[ii]), str(topics[ii]), str(blocks[ii]))
                ii += 1
        except BaseException as err:
                print("Exception.  " + str(err))

        #TODO: Change logic!!!
        #TODO: Change logic!!!
        #TODO: Change logic!!!
        #TODO: Change logic!!!

        #Cleaning duplicates
        
        # initializing MySQL connection #1
        try:
          my_cn = mysql.connector.connect(**my_config)
        except mysql.connector.Error as err:
            print(err)
            quit()
        else:
          print ("Connected to the Database #1")

        # initializing MySQL connection #2
        try:
          my_cn2 = mysql.connector.connect(**my_config)
        except mysql.connector.Error as err:
            print(err)
            quit()
        else:
          print ("Connected to the Database #2")


        # initializing MySQL connection #3
        try:
          my_cn3 = mysql.connector.connect(**my_config)
        except mysql.connector.Error as err:
            print(err)
            quit()
        else:
          print ("Connected to the Database #3")



        cursor =  my_cn.cursor() 
        cursor2 =  my_cn2.cursor()
        cursor3 = my_cn3.cursor()

        # Making a consolidated array of addresses

        # Read contracts into array

        c_sql="select pair from cur_pair"
        cursor.execute(c_sql)
        for c in cursor:
            cur_name = c[0]


        c_sql = "select pair_id from test_info where pair_id > %s order by pair_id"
        cursor.execute(c_sql, [cur_name])
        for c in cursor:
            try:
                pair = pairs(c[1].strip())
                cursor2.execute('update cur_pair set pair = %s', [ c[1] ])
                my_cn2.commit()
                if pair != c[0]:
                    print(c[0] + '---' + c[1] + '---' + str(pair) + '--- ERROR')
                    cursor3.execute('insert into audit (pair, pair_id, message) values (%s, %s, %s)', [ c[0], c[1], 'ERROR' ])
                    my_cn3.commit()
                else:
                    print(c[0] + '---' + c[1] + '---' + str(pair) + '--- OK')
            except BaseException as err:
                print(c[0] + '---' + c[1] + '---' + str(pair) + '--- Exception ' + str(err))
                cursor3.execute('insert into audit (pair, pair_id, message) values (%s, %s, %s, %s)', [ c[0], c[1], 'Exception '+str(err) ])
                my_cn3.commit()
    

        # Clean the database
        cursor3.execulte('delete from server.test_info where addr in (select pair_id from audit)')
        my_cn3.commit()
        cursor3.execute('delete from server.audit')
        my_cn3.commit()
        
        # Close the cursor and the connection
        cursor.close()
        my_cn.close()

        cursor2.close()
        my_cn2.close()

        cursor3.close()
        my_cn3.close()

    return crud.create_pair(db=db, pair=pair)


@app.get("/pairs/", response_model=List[schemas.Pair])
def read_pairs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pairs = crud.get_pairs(db, skip=skip, limit=limit)
    return pairs

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# Close the cursor and the connection
cursor0.close()
my_cn.close()