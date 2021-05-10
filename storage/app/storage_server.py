import capsule.storage_pb2 as storage_pb2
import capsule.storage_pb2_grpc as storage_pb2_grpc
import capsule.common_pb2 as common_pb2
import capsule.common_pb2_grpc as common_pb2_grpc
import capsule.scheduler_pb2 as scheduler_pb2
import capsule.scheduler_pb2_grpc as scheduler_pb2_grpc
import hashlib
import time
import os
import random
import grpc 
from concurrent import futures
import sqlite3
import argparse
import logging

DATA_DIR = "./data"
class StorageServicer(storage_pb2_grpc.StorageServicer):
    def __init__(self):
        if not os.path.exists("./index.db"):
            con = sqlite3.connect("index.db")
            cur = con.cursor()
            # Create table
            cur.execute('''CREATE TABLE ID2PATH
                          (key blob, filepath text)''')
            con.commit()
            con.close()
        logging.info("Storage Service is up, the metadata are stored in the index.db, and all the snapshots are stored in ./data folder")

    def StoreContent(self, store_request, context):
        key = store_request.key
        data = store_request.data
        logging.info("StoreContent with key: ", store_request.key)
        # the path structure : DATA_DIR/key
        filepath = os.path.join(DATA_DIR, key)
        with open(filepath, "wb") as f:
            f.write(data)
        logging.info("storing content @ " + filepath)
        self.sql_store(key, filepath)
        return common_pb2.Empty()

    def GetContent(self, store_key, context):
        key = store_key.key
        logging.info("GetContent with key: ", key)
        con = sqlite3.connect("index.db")
        cur = con.cursor()
        # Insert a row of data
        cur.execute("SELECT * FROM ID2PATH WHERE key=?", (key,))
        content = cur.fetchone()
        if content is None:
            logging.info("getting no content")
            context.abort(grpc.StatusCode.NOT_FOUND, "key not found")
        _, path = content
        con.close()
        logging.info("getting content @ " + path)
        with open(path, "rb") as f:
            data = f.read()
        return storage_pb2.StoredData(data=data)
    
    def sql_store(self, key, filepath):
        con = sqlite3.connect("index.db")
        cur = con.cursor()
        # Insert a row of data
        cur.execute("INSERT INTO ID2PATH VALUES (?,?)", [key, filepath])
        con.commit()
        con.close()

def register(sched_addr, sched_port, addr, port):
    with grpc.insecure_channel(sched_addr + ':' + str(sched_port)) as channel:
        stub = scheduler_pb2_grpc.SchedulerStub(channel)
        stub.RegisterStorage(common_pb2.Endpoint(addr=addr, port=port))
        logging.info("successfully registered at "+ sched_addr + ":" + str(sched_port))

def serve(port="50050"):
    try:
        if not 1024 <= int(port) < 65536:
            print("invalid port number")
            return
    except:
        print("invalid port number")
        return 

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    storage_pb2_grpc.add_StorageServicer_to_server(
        StorageServicer(), server)
    server.add_insecure_port('[::]:'+port)
    server.start()
    logging.info("start server at port " + port + " successfully!")
    server.wait_for_termination()

if __name__ == '__main__':
    STORAGE_HOSTNAME = "archive-storage"
    STORAGE_PORT = 50050
    SCHEDULER_HOSTNAME = "archive-scheduler"
    SCHEDULER_PORT = "8848"
    register(SCHEDULER_HOSTNAME, SCHEDULER_PORT, STORAGE_HOSTNAME, STORAGE_PORT)
    serve()