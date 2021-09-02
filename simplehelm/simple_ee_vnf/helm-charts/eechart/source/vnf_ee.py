##
# Copyright 2019 Telefonica Investigacion y Desarrollo, S.A.U.
# This file is part of OSM
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For those usages not covered by the Apache License, Version 2.0 please
# contact with: nfvlabs@tid.es
##

import asyncio
import logging
import asyncssh


from osm_ee.exceptions import VnfException


class VnfEE:

    def __init__(self, config_params):
        self.logger = logging.getLogger('osm_ee.vnf')
        self.config_params = config_params

    async def config(self, id, params):
        self.logger.debug("Execute action config params: {}".format(params))
        # Config action is special, params are merged with previous config calls
        self.config_params.update(params)
        required_params = ["ssh-hostname"]
        self._check_required_params(self.config_params, required_params)
        yield "OK", "Configured"

    async def touch(self, id, params):
        self.logger.debug("Execute action touch params: '{}', type: {}".format(params, type(params)))

        try:
            self._check_required_params(params, ["file-path"])

            # Check if filename is a single file or a list
            file_list = params["file-path"] if isinstance(params["file-path"], list) else [params["file-path"]]
            file_list_length = len(file_list)

            async with asyncssh.connect(self.config_params["ssh-hostname"],
                                        password=self.config_params.get("ssh-password"),
                                        username=self.config_params.get("ssh-username"),
                                        known_hosts=None) as conn:
                for index, file_name in enumerate(file_list):
                    command = "touch {}".format(file_name)
                    self.logger.debug("Execute remote  command: '{}'".format(command))
                    result = await conn.run(command)
                    self.logger.debug("Create command result: {}".format(result))

                    if result.exit_status != 0:
                        detailed_status = result.stderr
                        # TODO - ok but with some errors
                    else:
                        detailed_status = "Created file {}".format(file_name)

                    if index + 1 != file_list_length:
                        yield "PROCESSING", detailed_status
                    else:
                        yield "OK", detailed_status
        except Exception as e:
            self.logger.error("Error creating remote file: {}".format(repr(e)))
            yield "ERROR", str(e)

    async def sleep(self, id, params):
        self.logger.debug("Execute action sleep, params: {}".format(params))

        for i in range(3):
            await asyncio.sleep(5)
            self.logger.debug("Temporal result return, params: {}".format(params))
            yield "PROCESSING", f"Processing {i} action id {id}"
        yield "OK", f"Processed action id {id}"

    @staticmethod
    def _check_required_params(params, required_params):
        for required_param in required_params:
            if required_param not in params:
                raise VnfException("Missing required param: {}".format(required_param))
