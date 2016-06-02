FROM jupyter/minimal-notebook
MAINTAINER Ziv Dreyfuss "ziv@uchicago.edu"

# proxy environment variables
ENV https_proxy='http://cloud-proxy:3128'
ENV http_proxy='http://cloud-proxy:3128'

# give notebook user sudo priviledges
USER root
RUN echo "$NB_USER ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/notebook

# pass proxy environment variables to sudo
RUN echo 'Defaults env_keep = "http_proxy https_proxy"' >> /etc/sudoers.d/notebook

# erase /etc/apt/sources.list
# replace with US, Debian Jessie repositories (generated from 'https://debgen.simplylinux.ch')
# also, include backports repository (for docker installation)
RUN printf "deb http://ftp.us.debian.org/debian/ jessie main\ndeb-src http://ftp.us.debian.org/debian/ jessie main\n\ndeb http://security.debian.org/ jessie/updates main\ndeb-src http://security.debian.org/ jessie/updates main\n\ndeb http://ftp.debian.org/debian jessie-backports main" > /etc/apt/sources.list

# switch back to jovyan
USER $NB_USER

# get packages from repositories we just added to /etc/apt/sources.list
RUN sudo apt-get update

# install sudo 
RUN sudo apt-get install -y sudo

# install docker
RUN sudo apt-get -y -t jessie-backports install 'docker.io'

CMD ["jupyter","notebook","--no-browser"]
