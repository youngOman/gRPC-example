from typing import cast

import grpc

import calculator_pb2
import calculator_pb2_grpc


def run_client():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = calculator_pb2_grpc.CalculatorStub(channel)

        # 測試加法 API: a=10, b=5, 預期結果=16 (10+5+1)
        print("測試加法 API:")
        request = calculator_pb2.CalculatorRequest(a=10, b=5)
        response = cast("calculator_pb2.CalculatorResponse", stub.Add(request))
        print(f"Add(10, 5) = {response.result} (預期: 16)")

        # 測試減法 API: a=10, b=5, 預期結果=4 (10-5-1)
        print("\n測試減法 API:")
        request = calculator_pb2.CalculatorRequest(a=10, b=5)
        response = cast("calculator_pb2.CalculatorResponse", stub.Subtract(request))
        print(f"Subtract(10, 5) = {response.result} (預期: 4)")

        # 額外測試案例
        print("\n額外測試案例:")

        # 加法: a=20, b=15, 預期結果=36 (20+15+1)
        request = calculator_pb2.CalculatorRequest(a=20, b=15)
        response = cast("calculator_pb2.CalculatorResponse", stub.Add(request))
        print(f"Add(20, 15) = {response.result} (預期: 36)")

        # 減法: a=100, b=30, 預期結果=69 (100-30-1)
        request = calculator_pb2.CalculatorRequest(a=100, b=30)
        response = cast("calculator_pb2.CalculatorResponse", stub.Subtract(request))
        print(f"Subtract(100, 30) = {response.result} (預期: 69)")


if __name__ == "__main__":
    run_client()
