FROM nikolaik/python-nodejs
WORKDIR /usr/src/app
EXPOSE 50051

# install grpc
RUN pip install --no-cache-dir grpcio-tools grpcio

RUN apt-get update
# install curl for singlefile
RUN apt install curl -y
# install wget for pdf
RUN apt-get install wget -y
RUN apt-get install ffmpeg -y
# install youtube-dl for video
# RUN curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
# RUN chmod a+rx /usr/local/bin/youtube-dl

# RUN apt-get install sudo -y
# ####
# RUN mkdir data
# RUN /usr/bin/docker -h
# #### 

# RUN groupadd archivebox
# RUN useradd -r -g archivebox -G audio,video archivebox
# RUN chown -R archivebox:archivebox .

# RUN chown -R archivebox:archivebox /home
# ENV ALL_PROXY  'http://172.17.0.1:9000'
# ENV http_proxy "http://172.17.0.1:9000"
# ENV HTTP_PROXY "http://172.17.0.1:9000"
# ENV https_proxy "http://172.17.0.1:9000"
# ENV HTTPS_PROXY "http://172.17.0.1:9000"

# # RUN ping 172.17.0.1
# # RUN curl google.com
# RUN echo 'haha'
# RUN sudo -u archivebox archivebox init --setup
# RUN archivebox add www.baidu.com
# RUN sudo -u archivebox archivebox setup
# RUN ls /etc/sudoers.d
# RUN sudo echo "archivebox  ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/archivebox
# RUN sudo chmod 0440 /etc/sudoers.d/archivebox
# RUN curl -sSL 'https://get.archivebox.io' | sudo -u archivebox sh

# ENV ALL_PROXY=
# ENV http_proxy=
# ENV HTTP_PROXY=
# ENV https_proxy=
# ENV HTTPS_PROXY=
COPY app ./
RUN make
CMD ["python3", "worker_server.py"]

