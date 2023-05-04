import queue
import threading
import time
from concurrent import futures
from dataclasses import dataclass
from datetime import datetime

import grpc

from mock_data import MockDataGenerator
from pb2 import stock_exchange_pb2, stock_exchange_pb2_grpc
from pb2.stock_exchange_pb2 import SubPctChangeRequest, SubRequest


@dataclass
class ClientSubscription:
    context: grpc.ServicerContext
    queue: queue.Queue
    symbols: list

    pct_change: bool = False
    pct_change_threshold: float = 0.0

    status: str = "active"
    last_sent: int | None = None


class StockExchange(stock_exchange_pb2_grpc.StockExchangeServicer):
    def __init__(self):
        self.subscriptions = []
        self.running = True
        threading.Thread(target=self.queue_updates).start()
        threading.Thread(target=self.print_subscriptions).start()

    def queue_updates(self):
        while self.running:
            for sub in self.subscriptions:
                if sub.pct_change:
                    for symbol in sub.symbols:
                        stock_data = MockDataGenerator.get_stock_data(symbol)
                        if abs(stock_data.pct_change) > sub.pct_change_threshold:
                            sub.queue.put(stock_exchange_pb2.StockDataResponse(data={symbol: stock_data}))
                else:
                    for symbol in sub.symbols:
                        stock_data = MockDataGenerator.get_stock_data(symbol)
                        sub.queue.put(stock_exchange_pb2.StockDataResponse(data={symbol: stock_data}))
            time.sleep(1)

    def _validate_subscription(self, request, context):
        if request.symbols is None or len(request.symbols) == 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "No symbols provided")
        if any([s not in MockDataGenerator.get_available_symbols() for s in request.symbols]):
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Invalid symbol")
            print(f"Client {context.peer()} requested invalid symbol")
            return False

        return True

    def Subscribe(self, request: SubRequest, context: grpc.ServicerContext):
        if not self._validate_subscription(request, context):
            return

        print(f"Client {context.peer()} subscribed to {request.symbols}")

        sub = ClientSubscription(
            context=context,
            queue=queue.Queue(),
            symbols=list(request.symbols)
        )
        self.subscriptions.append(sub)

        return self._generate_responses(sub)

    def SubscribeOnPctChange(self, request: SubPctChangeRequest, context: grpc.ServicerContext):
        print(f"Client  {context.peer()} trynna sub to {request.symbols} "
              f"with pct_change_threshold={request.pct_change}")
        if not self._validate_subscription(request, context):
            return

        print(f"Client {context.peer()} subscribed to {request.symbols} "
              f"with pct_change_threshold={request.pct_change}")

        sub = ClientSubscription(
            context=context,
            queue=queue.Queue(),
            symbols=list(request.symbols),
            pct_change=True,
            pct_change_threshold=request.pct_change
        )
        self.subscriptions.append(sub)

        return self._generate_responses(sub)

    def Ping(self, request: stock_exchange_pb2.Empty, context: grpc.ServicerContext):
        return stock_exchange_pb2.Empty()

    def _generate_responses(self, sub: ClientSubscription):
        try:
            while True:
                if not sub.context.is_active():
                    sub.status = "inactive"
                    if int(time.time()) - sub.last_sent > 30:
                        print(f"Client {sub.context.peer()} inactive for 30 seconds, removing subscription")
                        self.subscriptions.remove(sub)
                        break
                    time.sleep(1)
                    continue
                else:
                    sub.status = "active"

                try:
                    response = sub.queue.get(timeout=1)
                    sub.last_sent = int(time.time())
                    yield response
                except queue.Empty:
                    continue

        except grpc.RpcError:
            print(f"Client disconnected: {sub.context.peer()}")
            self.subscriptions.remove(sub)

    def stop(self):
        print("Stopping server...")
        self.running = False

    def print_subscriptions(self):
        while self.running:
            time.sleep(1)
            if not self.subscriptions:
                continue

            print(f"Subscriptions: {datetime.now()}")
            for sub in self.subscriptions:
                time_since_last_sent = int(int(time.time()) - sub.last_sent) if sub.last_sent else "N/A"
                sub_type = "pct_change" if sub.pct_change else "regular"
                print(
                    f"  {sub.context.peer()}  |  {sub_type}  |  {sub.status}  |  {time_since_last_sent}s  | {sub.symbols}")
            print("-----------------------------------")


if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
    stock_exchange_pb2_grpc.add_StockExchangeServicer_to_server(StockExchange(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started, listening on 50051")

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
