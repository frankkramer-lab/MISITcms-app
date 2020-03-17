#!/bin/bash
old_cwd=$(pwd)
cd $(dirname "$0")

openssl req -new -newkey rsa:4096 -sha256 -nodes -x509 -keyout ./nginx/cms.key -out ./nginx/cms.crt -subj "/C=DE/ST=Bayern/L=Augsburg/O=Universität Augsburg/OU=Misit/CN=*.informatik.uni-augsburg.de"

cd $old_cwd
