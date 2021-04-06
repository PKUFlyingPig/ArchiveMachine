import os
import storage_pb2
import storage_pb2_grpc
import grpc

def example_store_client(stub, filepath):
    with open(filepath, "rb") as file:
        content = file.read()
    print("store " + filepath + " onto the storage server ... ...")
    snapid = stub.StoreContent(storage_pb2.Content(url="https://www.baidu.com", timestamp="2021-4-6", data=content))
    print("successfully stored, get the snapshot id:")
    print(snapid.id)
    return str(snapid.id)

def example_get_client(stub, snapshot_id):
    contents = stub.GetContent(storage_pb2.SnapshotID(id=snapshot_id))
    print(contents.url, contents.timestamp)

if __name__ == '__main__':
    with grpc.insecure_channel('localhost:50050') as channel:
        stub = storage_pb2_grpc.StorageStub(channel)
        snapshot_id = example_store_client(stub, "../worker/tmpdata/test.html")
        example_get_client(stub, snapshot_id)

