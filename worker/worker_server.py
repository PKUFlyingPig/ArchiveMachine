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
from utils import add_url, ip4_addresses
import argparse
import logging

class WorkerServicer(worker_pb2_grpc.WorkerServicer):
    def CrawlUrl(self, Url, context):
        saved_path = add_url(Url.url)
        with open(os.path.join(saved_path,"singlefile.html"), 'rb') as content_file:
            content = content_file.read()
        return common_pb2.Content(data=content)

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
    logging.basicConfig(logging.INFO)
    parser = argparse.ArgumentParser(description='Start worker server')
    parser.add_argument("-a", "--addr", help="ip address of the scheduler", type=str, default="127.0.0.1")
    parser.add_argument("-p", "--port", help="port number of the scheduler", type=int, default="8000")
    args = parser.parse_args()

    ipaddrs = ip4_addresses()
    if len(ipaddrs) is None:
        logging.log("no host ip addr available")
    else:
        print("available host addr: ", ipaddrs)
        register(args.addr, args.port, ipaddrs, 50051)
        serve()