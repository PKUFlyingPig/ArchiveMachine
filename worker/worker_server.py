from concurrent import futures
import os
import grpc
import worker_pb2
import worker_pb2_grpc
from utils import add_url

class WorkerServicer(worker_pb2_grpc.WorkerServicer):
    def CrawlUrl(self, Url, context):
        saved_path = add_url(Url.url)
        with open(os.path.join(saved_path,"singlefile.html"), 'rb') as content_file:
            content = content_file.read()
        yield worker_pb2.Content(data=content)

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
    serve()