#!/bin/bash
# Author: Gabriel Vázquez Torres @gabvaztor
###  Control will jump here if $DIR does NOT exists ###
echo "***************************"
echo "**DOCKER INSTALLATION STARTED...**"
echo "***************************"

sudo yum update -y
sudo amazon-linux-extras install docker
sudo service docker start
# change this if needed
sudo usermod -a -G docker ec2-user

echo ""
echo "***************************"
echo "** DOCKER INSTALLATION FINISHED **"
echo "***************************"
