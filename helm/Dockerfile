FROM centos:7
RUN yum update -y
RUN yum install -y curl
RUN curl -o helm3.tar.gz https://get.helm.sh/helm-v3.0.0-alpha.1-linux-amd64.tar.gz
RUN tar -xf helm3.tar.gz linux-amd64/helm && \
    mv linux-amd64/helm /usr/local/bin
