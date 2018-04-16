FROM node:9.10.1
MAINTAINER TzLibre "tzlibre@mail.com"

COPY gen-signatures.sh /tmp
ADD pykeychecker /tmp/pykeychecker/
ADD jstxencoder /tmp/jstxencoder/
RUN wget https://download.libsodium.org/libsodium/releases/libsodium-1.0.16.tar.gz; \
    tar xfz libsodium-1.0.16.tar.gz; \
    cd libsodium-1.0.16; \
    ./configure; \
    make -j2; \
    make install
RUN apt-get update; apt-get -y install python-dev python-pip

WORKDIR /tmp
RUN cd pykeychecker; pip install -r requirements.txt
RUN cd jstxencoder; npm install

CMD bash gen-signatures.sh
