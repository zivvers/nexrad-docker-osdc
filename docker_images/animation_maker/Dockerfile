FROM ubuntu
ENV https_proxy='http://cloud-proxy:3128'
ENV http_proxy='http://cloud-proxy:3128'

RUN apt-get update
RUN apt-get install -y python
RUN apt-get install -y libav-tools
RUN apt-get install -y python-qt4
RUN apt-get install -y python-pip

RUN pip install ipython
RUN pip install --upgrade pip
RUN apt-get install -y libfreetype6-dev
RUN apt-get install -y libpng-dev
RUN apt-get install pkg-config
RUN pip install matplotlib
#apt-get install python-matplotlib
# install ipython for testing purposes
#RUN apt-get install -y ipython
#RUN apt-get install -y python-matplotlib
RUN apt-get install -y libjpeg8-dev
RUN pip install Pillow
RUN apt-get install ffmpeg
