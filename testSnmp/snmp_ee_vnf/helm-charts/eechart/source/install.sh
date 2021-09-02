#!/bin/bash
##
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
##

echo "installing libraries for snmp generator"

#apt-get install -y ...
apt-get update

apt-get install -y python3-pip unzip build-essential libsnmp-dev wget curl
curl -s https://storage.googleapis.com/golang/go1.11.8.linux-amd64.tar.gz | tar -v -C /usr/local -xz
export PATH=$PATH:/usr/local/go/bin
export GOPATH=/go

go get github.com/go-logfmt/logfmt && go get github.com/go-kit/kit/log

wget -q https://github.com/prometheus/snmp_exporter/archive/v0.17.0.tar.gz -P /tmp/ \
&& tar -C /tmp -xf /tmp/v0.17.0.tar.gz \
&& (cd /tmp/snmp_exporter-0.17.0/generator && go build) \
&& cp /tmp/snmp_exporter-0.17.0/generator/generator /usr/local/bin/snmp_generator

