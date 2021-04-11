"""
client side code
"""
import grpc
import os
import capsule.worker_pb2_grpc as worker_pb2_grpc
import capsule.worker_pb2 as worker_pb2
import capsule.common_pb2_grpc as common_pb2_grpc
import capsule.common_pb2 as common_pb2

DATA_DIR = "./tmpdata/"
def client(stub, url, output="test.html"):
    print("call the server for " + url)
    content = stub.CrawlUrl(common_pb2.Url(url=url))
    with open(os.path.join(DATA_DIR, output), 'wb') as f:
        f.write(content.data)
    print("successfully crawl the URL: " + url)
    print("the output is saved into " + os.path.join(DATA_DIR, output))
    # except:
    #     print("!!Failed to request the URL: " + url + " !!")


if __name__ == '__main__':
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = worker_pb2_grpc.WorkerStub(channel)
        client(stub, "https://www.baidu.com", "newtest.html")
