FROM python:3
WORKDIR /usr/src/app
EXPOSE 50051

RUN pip install --no-cache-dir grpcio-tools grpcio

COPY app ./
RUN make
CMD ["python3", "storage_server.py"]

