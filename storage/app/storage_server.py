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
                          (key blob, data blob)''')
            con.commit()
            con.close()
        logging.info("Storage Service is up, the metadata are stored in the index.db, and all the snapshots are stored in ./data folder")

    def StoreContent(self, contents, context):
        logging.info("StoreContent with uuid: ", contents.meta.uuid)
        meta = contents.meta
        data = contents.data
        # the path structure : DATA_DIR/url#current Linux time#.html
        filepath = os.path.join(DATA_DIR, meta.url.url.split("/")[-1]+"#"+str(meta.timestamp)+"#.html")
        with open(filepath, "wb") as f:
            f.write(data)
        logging.info("storing content @ " + filepath)
        self.sql_store(meta, filepath)
        return common_pb2.Empty()

    def GetContent(self, snapshot, context):
        logging.info("GetContent with uuid: ", snapshot.uuid)
        con = sqlite3.connect("index.db")
        cur = con.cursor()
        # Insert a row of data
        cur.execute("SELECT * FROM ID2PATH WHERE uuid=?", (snapshot.uuid,))
        content = cur.fetchone()
        if content is None:
            logging.info("getting no content")
            context.abort(grpc.StatusCode.NOT_FOUND, "uuid not found")
        uuid, digest, url, timestamp, path = content
        con.close()
        logging.info("getting content @ " + path)
        with open(path, "rb") as f:
            data = f.read()
        meta = common_pb2.Snapshot(uuid=uuid, hash=digest, url=common_pb2.Url(url=url),timestamp=timestamp)
        return common_pb2.Content(meta=meta, data=data)
    
    def sql_store(self, meta, filepath):
        con = sqlite3.connect("index.db")
        cur = con.cursor()
        # Insert a row of data
        cur.execute("INSERT INTO ID2PATH VALUES (?,?,?,?,?)", [meta.uuid, meta.hash, meta.url.url, meta.timestamp, filepath])
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