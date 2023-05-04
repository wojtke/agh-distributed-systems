mkdir -p ./pb2
echo "import sys" > ./pb2/__init__.py
echo "from pathlib import Path" >> ./pb2/__init__.py
echo "sys.path.append(str(Path(__file__).parent))" >> ./pb2/__init__.py
python -m grpc_tools.protoc \
          -I../proto \
          --python_out=./pb2 \
          --pyi_out=./pb2 \
          --grpc_python_out=./pb2 \
          ../proto/stock_exchange.proto