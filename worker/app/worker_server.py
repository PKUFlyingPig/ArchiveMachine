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

class WorkerServicer(worker_pb2_grpc.WorkerServicer):
    def CrawlUrl(self, crawl_request, context):
        for url in crawl_request.urls:
            saved_path = add_url(url)
            with open(os.path.join(saved_path,"singlefile.html"), 'rb') as content_file:
                data = content_file.read()
            content = common_pb2.Content(type=common_pb2.Content.Type.html, data=data)
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
    print("start server at port " + port + " successfully!")
    server.wait_for_termination()

if __name__ == '__main__':
    WORKER_HOSTNAME = "archive-worker"
    WORKER_PORT = 50051
    SCHEDULER_HOSTNAME = "archive-scheduler"
    SCHEDULER_PORT = "8848"
    
    print("worker hostname :", WORKER_HOSTNAME)
    register(SCHEDULER_HOSTNAME, SCHEDULER_PORT, WORKER_HOSTNAME, WORKER_PORT)
    serve()