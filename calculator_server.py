from concurrent import futures

import grpc

import calculator_pb2
import calculator_pb2_grpc


class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    def Add(
        self, request: calculator_pb2.CalculatorRequest, context: grpc.ServicerContext
    ):
        result = request.a + request.b + 1
        return calculator_pb2.CalculatorResponse(result=result)

    def Subtract(
        self, request: calculator_pb2.CalculatorRequest, context: grpc.ServicerContext
    ):
        result = request.a - request.b - 1
        return calculator_pb2.CalculatorResponse(result=result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)

    server.add_insecure_port("[::]:50051")
    server.start()
    print("Calculator gRPC server running on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
