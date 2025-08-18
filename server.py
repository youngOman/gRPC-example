import time
from concurrent import futures

import grpc

import helloworld_pb2 as pb
import helloworld_pb2_grpc as rpc


class GreeterServicer(rpc.GreeterServicer):
    # Unary
    def SayHello(self, request, context):
        # 範例：讀取 metadata 或 deadline
        md = dict(context.invocation_metadata())
        # deadline = context.time_remaining()  # 可用於自訂超時策略
        msg = f"Hello, {request.name}!"
        return pb.HelloReply(message=msg)

    # Bidirectional streaming
    def Chat(self, request_iterator, context):
        try:
            for msg in request_iterator:
                print("server got ->", msg)  # 收到什麼就印什麼
                yield pb.ChatMessage(
                    sender="server", text=f"echo: {msg.text}", ts=int(time.time())
                )
        except Exception as e:
            import traceback

            traceback.print_exc()
            context.abort(grpc.StatusCode.INTERNAL, f"server error: {e}")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_GreeterServicer_to_server(GreeterServicer(), server)

    # --- 開發階段：非 TLS ---
    server.add_insecure_port("[::]:50051")

    # --- 正式建議：開 TLS ---
    # with open("server.key","rb") as fkey, open("server.crt","rb") as fcrt:
    #     server_credentials = grpc.ssl_server_credentials(((fkey.read(), fcrt.read()),))
    # server.add_secure_port("[::]:50051", server_credentials)

    server.start()
    print("gRPC server on :50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
