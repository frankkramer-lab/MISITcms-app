FROM ubuntu:18.04

WORKDIR /root
ADD ./wait-for-it.sh ./wait-for-it.sh
# Setup system environment variables
ENV DEBIAN_FRONTEND=noninteractive

RUN ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime

RUN apt-get update && \
    apt-get install -y build-essential openjdk-8-jdk-headless fp-compiler \
                postgresql-client python3.6 python3.6-dev python3-pip cppreference-doc-en-html \
		cgroup-lite libcap-dev zip sudo libpq-dev libcups2-dev libyaml-dev \
		libffi-dev git && \
    apt-get install -y python3-setuptools python3-tornado python3-psycopg2 \
		python3-sqlalchemy python3-psutil python3-netifaces python3-crypto \
		python3-bs4 python3-coverage python3-requests python3-werkzeug \
		python3-gevent python3-bcrypt python3-chardet patool python3-babel \
		python3-xdg python3-jinja2 && \
    \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Add UTF-8 as default language encoding
# RUN locale-gen en_US.UTF-8
ENV LC_ALL="en_US.UTF-8"
ENV LANG="en_US.UTF-8"
ENV LANGUAGE="en_US.UTF-8"

RUN git clone https://github.com/cms-dev/cms.git -b master --recursive && cd cms && git checkout d4c9e926bd52d8022069c417b206b0882ef4d1ba
RUN cd cms && python3 setup.py install
RUN pip3 install -r cms/requirements.txt

RUN mkdir -p /var/log/cms

CMD ["/bin/bash"]


