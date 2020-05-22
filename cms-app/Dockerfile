#-----------------------------------------------------#
#              Information & System Base              #
#-----------------------------------------------------#
FROM ubuntu:18.04
WORKDIR /root
ADD ./wait-for-it.sh ./wait-for-it.sh

LABEL authors="Johann Frei, Dominik Müller"
LABEL contact="dominik.mueller@informatik.uni-augsburg.de"
LABEL repository="https://github.com/frankkramer-lab/MISITcms-app"
LABEL license="GNU General Public License v3.0"

#-----------------------------------------------------#
#                     System Setup                    #
#-----------------------------------------------------#
# Setup system environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Adjust timezone
RUN ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime

# Install required software
RUN apt-get update && \
    apt-get install -y locales build-essential openjdk-8-jdk-headless fp-compiler \
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
RUN locale-gen "en_US.UTF-8"

#-----------------------------------------------------#
#                      CMS Setup                      #
#-----------------------------------------------------#
# Get CMS repository params
ARG CMS_REPOSITORY_URL='https://github.com/frankkramer-lab/MISITcms.git'
ARG CMS_REPOSITORY_BRANCH='master'
ARG CMS_CHECKOUT=''

# Install CMS
RUN git clone ${CMS_REPOSITORY_URL} -b ${CMS_REPOSITORY_BRANCH} --recursive cms
RUN cd cms && git checkout ${CMS_CHECKOUT}
RUN cd cms && pip3 install -r requirements.txt
RUN cd cms && python3 prerequisites.py --as-root build
RUN cd cms && python3 prerequisites.py --as-root install
RUN cd cms && python3 setup.py install

# Setup CMS environment variables
ENV PATH="${PATH}:/root/cms/isolate/"
ENV PYTHONPATH="/root/cms/"

# Further initializations
RUN mkdir -p /var/log/cms

#-----------------------------------------------------#
#                   Finish & Startup                  #
#-----------------------------------------------------#
# Dev-Comment: add docker entrypoint later (instead of mounting)

CMD ["/bin/bash"]
