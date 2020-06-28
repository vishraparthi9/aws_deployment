#!/bin/bash

exec > >(tee -i /var/log/user-data.log)
exec 2>&1

yum install -y unzip

cd /tmp/ && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && sudo ./aws/install

cd /tmp/ && curl -L -O https://www.getchef.com/chef/install.sh && chmod 755 install.sh && ./install.sh && rm -f install.sh

aws s3 cp s3://vraparthi-cicd-testing/helloworld_chef/helloworld-${CI_GIT_COMMIT}-${CD_GIT_COMMIT}.tar.gz /tmp/

tar -xzf /tmp/helloworld-${CI_GIT_COMMIT}-${CD_GIT_COMMIT}.tar.gz

cd /tmp/ && chef-client -z --chef-license 'accept' -c /tmp/.chef/config.rb