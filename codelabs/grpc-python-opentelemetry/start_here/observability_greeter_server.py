# Copyright 2024 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server for observability codelab."""

from concurrent import futures
import logging
import time

import grpc
import helloworld_pb2
import helloworld_pb2_grpc

_SERVER_PORT = "50051"


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        message = request.name
        # CODELAB HINT: This sleep seems suspicious.
        time.sleep(5)
        return helloworld_pb2.HelloReply(message=f"Hello {message}")


def serve():
    # CODELAB HINT : Add code to register gRPC OpenTelemetry plugin here.
    server = grpc.server(
        thread_pool=futures.ThreadPoolExecutor(max_workers=10),
    )
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port("[::]:" + _SERVER_PORT)
    server.start()
    print("Server started, listening on " + _SERVER_PORT)

    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
