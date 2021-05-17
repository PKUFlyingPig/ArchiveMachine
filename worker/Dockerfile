FROM nikolaik/python-nodejs
WORKDIR /usr/src/app
EXPOSE 50051

RUN pip install --no-cache-dir grpcio-tools grpcio
RUN pip install archivebox
RUN apt-get update
RUN apt-get install sudo -y
RUN groupadd archivebox
RUN useradd -r -g archivebox -G audio,video archivebox
RUN chown -R archivebox:archivebox .

RUN chown -R archivebox:archivebox /home
# ENV ALL_PROXY  'http://172.17.0.1:9000'
# ENV http_proxy "http://172.17.0.1:9000"
# ENV HTTP_PROXY "http://172.17.0.1:9000"
# ENV https_proxy "http://172.17.0.1:9000"
# ENV HTTPS_PROXY "http://172.17.0.1:9000"

# RUN ping 172.17.0.1
# RUN curl google.com
RUN sudo -u archivebox archivebox init --setup

COPY app ./
RUN make
CMD ["python3", "worker_server.py"]

