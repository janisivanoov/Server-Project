#imports
import http.server
import socketserver
import urllib.request
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
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, create_engine
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request, Response, Depends
from fastapi.responses import HTMLResponse
from uint import Uint, Int
from pydantic import BaseModel
from sqlalchemy.orm import relationship , Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

models.Base.metadata.create_all(bind=engine)



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




# SERVER PART



# FastAPI 

#database.py

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Model(ORM).py

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
    pair_id: int

    class Config:
        orm_mode = True

def get_pair(db: Session, pair_id: int):
    return db.query(models.Pair).filter(models.Pair.id == pair_id).first()

#crud.py

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

#main.oy

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
                # delete
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

    # Read contracts into array

    contracts = []
    c_sql = "select topic from ttopics"
    cursor.execute(c_sql)
    for c in cursor:
        contracts.append(c)


    aaa = []
    bbb = []
    ccc = []
    i=0
    for c in contracts:   
        print("Processing " + c[0])

        # Get transactions

        url ='https://api.etherscan.io/api?module=account&action=txlist&address='+c[0]+'&startblock='+str(getBlock(c[0]))+'&sort=asc&apikey='+eth_key
        req = urllib.request.urlopen(url)
        resp = req.read()
        tr = json.loads(resp)
        for txh in tr["result"]:
            aaa.append(Web3.toChecksumAddress(txh["from"]))
            bbb.append(txh["blockNumber"])
            ccc.append(c[0])
            i += 1


    b = 0

    # loop with maxcount step

    while (b+maxcount<len(aaa)):
        addresses = aaa[b:b+maxcount]
        blocks = bbb[b:b+maxcount]
        contracts = ccc[b:b+maxcount]

        # resolving and saving stop
        try:
                names = rrcontract.functions.getNames(addresses).call()
                ii = 0
                for n in names:
                    print(addresses[ii] + "---" + n)
                    updateName(str(n), str(addresses[ii]), str( contracts[ii]), str(blocks[ii]))
                    ii += 1
        except BaseException as err:
                print("Exception. Cannot  " + str(err))
        b += maxcount

    # resolving and saving remaining addresses

    addresses = aaa[b:len(aaa)-1]
    blocks = bbb[b:len(bbb)-1]
    contracts = ccc[b:len(ccc)-1]
    try:
        names = rrcontract.functions.getNames(addresses).call()
        ii = 0
        for n in names:
            print(addresses[ii] + "---" + n)
            updateName(str(n), str(addresses[ii]), str( contracts[ii]), str(blocks[ii]))
            ii += 1
    except BaseException as err:
            print("Exception. Cannot resolve names  " + str(err))

    return crud.create_pair(db=db, pair=pair)


@app.get("/pairs/", response_model=List[schemas.Pair])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
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
cursor.close()
my_cn.close()