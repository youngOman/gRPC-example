import logging
import time

import grpc

import helloworld_pb2 as pb
import helloworld_pb2_grpc as rpc

logging.basicConfig(level=logging.DEBUG)


def gen():
    try:
        for text in ["hi", "gRPC!", "這是雙向串流"]:
            msg = pb.ChatMessage(sender="client", text=text, ts=int(time.time()))
            print("client sending ->", msg)  # 重要：建構＋印出
            yield msg
            time.sleep(0.2)
    except Exception as e:
        print("GEN ERROR:", repr(e))
        raise


def bidi_stream():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = rpc.GreeterStub(channel)
        for reply in stub.Chat(gen(), timeout=30.0):
            print("Chat <-", reply.text)


if __name__ == "__main__":
    # 先測 unary（已通過）
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = rpc.GreeterStub(channel)
        print(stub.SayHello(pb.HelloRequest(name="早上好，現在我有冰淇淋!")).message)

    # 再測雙向
    bidi_stream()
