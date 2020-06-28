#!/bin/bash

yum install -y unzip

cd /tmp/ && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && sudo ./aws/install

cd /tmp/ && curl -L -O https://www.getchef.com/chef/install.sh && chmod 755 install.sh && ./install.sh && rm -f install.sh

aws s3 cp s3://vraparthi-cicd-testing/helloworld_chef/helloworld-$1-$2.tar.gz /tmp/

tar -xzf /tmp/helloworld-$1-$2.tar.gz

cd /tmp/ && chef-client -z --chef-license 'accept' -c /tmp/.chef/config.rb