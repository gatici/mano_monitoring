#!/bin/bash
##
# Copyright 2015 Telefonica Investigacion y Desarrollo, S.A.U.
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

# This script is intended for launching RO from a docker container.
# It waits for mysql server ready, normally running on a separate container, ...
# then it checks if database is present and creates it if needed.
# Finally it launches RO server.

echo "Sample install.sh from source dir"

# Install libraries
#apt-get install -y ...

# Install library to execute command remotely by ssh
python3 -m pip install asyncssh

