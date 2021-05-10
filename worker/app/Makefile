# https://github.com/grpc/grpc/issues/9575#issuecomment-293934506
generate:
	python3 -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/capsule/*.proto

clean:
	rm -rf capsule/
