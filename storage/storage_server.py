import storage_pb2
import storage_pb2_grpc
import hashlib
import time
import os
import random
import grpc 
from concurrent import futures
import sqlite3

DATA_DIR = "./data"
class StorageServicer(storage_pb2_grpc.StorageServicer):
    def __init__(self):
        if not os.path.exists("./index.db"):
            con = sqlite3.connect("index.db")
            cur = con.cursor()
            # Create table
            cur.execute('''CREATE TABLE ID2PATH
                          (SnapshotID text, Path text, URL text, TimeStamp text)''')
            con.commit()
            con.close()
        print("Storage Service is up, the (id, path) pairs are stored in the index.db, and all the snapshots are stored in ./data folder")

    def StoreContent(self, contents, context):
        url = contents.url
        timestamp = contents.timestamp
        content = contents.data
        # the path structure : DATA_DIR/url#current Linux time.html
        filepath = os.path.join(DATA_DIR, url.split("/")[-1]+"#"+timestamp+"#.html")
        with open(filepath, "wb") as f:
            f.write(content)
        s = hashlib.sha256()
        s.update((filepath + str(time.time())).encode())
        hashid = s.hexdigest()
        self.sql_store(hashid, filepath, url, timestamp)
        return storage_pb2.SnapshotID(id=hashid)

    def GetContent(self, SnapshotID, context):
        con = sqlite3.connect("index.db")
        cur = con.cursor()
        # Insert a row of data
        cur.execute("SELECT * FROM ID2PATH WHERE SnapshotID=?", (SnapshotID.id,))
        _, path, url, timestamp = cur.fetchone()
        con.close()
        with open(path, "rb") as f:
            content = f.read()
        return storage_pb2.Content(url=url, timestamp=timestamp, data=content)
    
    def sql_store(self, hashid, filepath, url, timestamp):
        con = sqlite3.connect("index.db")
        cur = con.cursor()
        # Insert a row of data
        cur.execute("INSERT INTO ID2PATH VALUES (?,?,?,?)", [hashid, filepath, url, timestamp])
        con.commit()
        con.close()


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
    print("start server at port " + port + " successfully!")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()