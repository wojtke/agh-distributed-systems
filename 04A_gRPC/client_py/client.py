import sys
import threading

import grpc
import argparse
from concurrent import futures
import time
from pb2 import stock_exchange_pb2
from pb2 import stock_exchange_pb2_grpc

_MAX_RETRIES = 5

def subscribe(client, symbols, attempt=1):
    def handle_response(response):
        print(f"Received stock data: {response}")

    try:
        for response in client.Subscribe(stock_exchange_pb2.SubRequest(symbols=symbols)):
            handle_response(response)
    except grpc.RpcError as e:
        if attempt <= _MAX_RETRIES:
            print(e)
            print(f"Attempt {attempt} failed, retrying...")
            time.sleep(2)
            subscribe(client, symbols, attempt + 1)
        else:
            print(f"Maximum retries reached, problem with the call: {e}")

def subscribe_on_pct_change(client, symbols, pct_change, attempt=1):
    def handle_response(response):
        print(f"Received stock data: {response}")

    try:
        for response in client.SubscribeOnPctChange(stock_exchange_pb2.SubPctChangeRequest(symbols=symbols, pct_change=pct_change)):
            handle_response(response)
    except grpc.RpcError as e:
        if attempt <= _MAX_RETRIES:
            print(e)
            print(f"Attempt {attempt} failed, retrying...")
            time.sleep(1)
            subscribe_on_pct_change(client, symbols, pct_change, attempt + 1)
        else:
            print(f"Maximum retries reached, problem with the call: {e}")

def ping(client):
    while True:
        try:
            client.Ping(stock_exchange_pb2.Empty())
            print("Ping successful")
        except grpc.RpcError as e:
            print(f"Error pinging server: {e}")
        time.sleep(10)

def main():
    parser = argparse.ArgumentParser(description="Stock Exchange Client")
    parser.add_argument("subscription_type", choices=["regular", "onchange"], help="Subscription type")
    parser.add_argument("args", nargs="+", help="Arguments for the subscription type")

    args = parser.parse_args()

    channel = grpc.insecure_channel('localhost:50051')
    client = stock_exchange_pb2_grpc.StockExchangeStub(channel)

    threading.Thread(target=ping, args=(client,)).start()

    if args.subscription_type == "regular":
        symbols = args.args
        subscribe(client, symbols)
    elif args.subscription_type == "onchange":
        pct_change = float(args.args[0])
        symbols = args.args[1:]
        subscribe_on_pct_change(client, symbols, pct_change)

if __name__ == "__main__":
    main()
