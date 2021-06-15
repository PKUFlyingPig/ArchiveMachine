from concurrent import futures
import os
import grpc
import capsule.worker_pb2 as worker_pb2
import capsule.worker_pb2_grpc as worker_pb2_grpc
import capsule.scheduler_pb2 as scheduler_pb2
import capsule.scheduler_pb2_grpc as scheduler_pb2_grpc
import capsule.common_pb2 as common_pb2
import capsule.common_pb2_grpc as common_pb2_grpc
import capsule.scheduler_pb2 as scheduler_pb2
import capsule.scheduler_pb2_grpc as scheduler_pb2_grpc
from utils import add_url
import argparse
import logging
import time
import random
import hashlib

STORE_SERVER = "https://storageserver.archive.xmcp.ltd/"
class WorkerServicer(worker_pb2_grpc.WorkerServicer):
    def Crawl(self, crawl_request, context):
        for url in crawl_request.urls:
            state = add_url(url)
            if state is None:
                continue
            source_type, filename = state
            show_url = (STORE_SERVER + filename).encode()
            # calculate hash
            with open(os.path.join('/usr/src/app/data', filename), 'rb') as f:
                rawdata = f.read()
                hashval = hashlib.sha256(rawdata).digest()
            
            if source_type == "html":
                content = common_pb2.Content(type=common_pb2.Content.Type.html, data=show_url, hash=hashval)
            elif source_type == "pdf":
                content = common_pb2.Content(type=common_pb2.Content.Type.pdf, data=show_url, hash=hashval)
            crawl_response = worker_pb2.CrawlResponse(url=url, content=content)
            yield crawl_response

def register(sched_addr, sched_port, addr, port):
    with grpc.insecure_channel(sched_addr + ':' + sched_port) as channel:
        stub = scheduler_pb2_grpc.SchedulerStub(channel)
        stub.RegisterWorker(common_pb2.Endpoint(addr=addr, port=port))
        print("successfully registered at "+ sched_addr + ":" + str(sched_port))

def serve(port="50051"):
    try:
        if not 1024 <= int(port) < 65536:
            print("invalid port number")
            return
    except:
        print("invalid port number")
        return 

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    worker_pb2_grpc.add_WorkerServicer_to_server(
        WorkerServicer(), server)
    server.add_insecure_port('[::]:'+port)
    server.start()
    logging.info("start server at port " + port + " successfully!")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    WORKER_HOSTNAME = "archive-worker"
    WORKER_PORT = 50051
    SCHEDULER_HOSTNAME = "archive-scheduler"
    SCHEDULER_PORT = "8848"
    MAX_REGISTERS = 20 
    for i in range(MAX_REGISTERS):
        try:
            register(SCHEDULER_HOSTNAME, SCHEDULER_PORT, WORKER_HOSTNAME, WORKER_PORT)
            time.sleep(1)
            break
        except:
            time.sleep(1)
    serve()