FROM continuumio/miniconda
MAINTAINER Ziv Dreyfuss "ziv@uchicago.edu"

ENV https_proxy='http://cloud-proxy:3128'
ENV http_proxy='http://cloud-proxy:3128'

RUN conda update conda
RUN conda install -c https://conda.binstar.org/jjhelmus pyart
RUN conda install basemap
