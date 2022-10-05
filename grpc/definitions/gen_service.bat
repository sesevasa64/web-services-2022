python -m grpc_tools.protoc -I definitions/ --python_betterproto_out=definitions/builds/^
 --grpc_python_out=definitions/builds/ definitions/checker.proto
