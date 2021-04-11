import os
import capsule.storage_pb2 as storage_pb2
import capsule.storage_pb2_grpc as storage_pb2_grpc
import capsule.common_pb2 as common_pb2
import capsule.common_pb2_grpc as common_pb2_grpc
import grpc

def example_store_client(stub, filepath):
    with open(filepath, "rb") as file:
        data = file.read()
    print("store " + filepath + " onto the storage server ... ...")
    meta = common_pb2.Snapshot(uuid=b'1111', hash=b'2222', url=common_pb2.Url(url="https://www.baidu.com"), timestamp=12345)
    stub.StoreContent(common_pb2.Content(meta=meta, data=data))
    print("successfully stored")

def example_get_client(stub, uuid):
    content = stub.GetContent(common_pb2.Snapshot(uuid=uuid))
    print("successfully get file")
    print(content.meta.hash, content.meta.url.url, content.meta.timestamp)

if __name__ == '__main__':
    with grpc.insecure_channel('localhost:50050') as channel:
        stub = storage_pb2_grpc.StorageStub(channel)
        example_store_client(stub, "../worker/tmpdata/test.html")
        example_get_client(stub, b"1111")

