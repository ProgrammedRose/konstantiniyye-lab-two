# src.app/grpc/server.py
import os

from grpc import aio

# imports of generated modules; they will be present after code generation step
from .protos import purchases_pb2_grpc, books_pb2_grpc
from src.app.grpc.handlers.books_handler import BookServiceServicer
from src.app.grpc.handlers.purchases_handler import PurchaseServiceServicer

GRPC_PORT = int(os.getenv("GRPC_PORT", "50051"))


async def serve():
    server = aio.server()
    books_pb2_grpc.add_BookServiceServicer_to_server(BookServiceServicer(), server)
    purchases_pb2_grpc.add_PurchaseServiceServicer_to_server(PurchaseServiceServicer(), server)
    listen_addr = f"[::]:{GRPC_PORT}"
    server.add_insecure_port(listen_addr)
    await server.start()
    print(f"gRPC server started on {listen_addr}")
    # do not await termination here — the event loop in FastAPI will keep process alive
    await server.wait_for_termination()
