##
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
##

import asyncio
import logging
import os


from osm_ee.exceptions import VnfException

import osm_ee.util.util_ee as util_ee


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

    async def sleep(self, id, params):
        self.logger.debug("Execute action sleep, params: {}".format(params))

        for i in range(3):
            await asyncio.sleep(5)
            self.logger.debug("Temporal result return, params: {}".format(params))
            yield "PROCESSING", f"Processing {i} action id {id}"
        yield "OK", f"Processed action id {id}"

    async def generate_snmp(self, id, params):
        self.logger.debug("Executing SNMP exporter configuration generation\nWith params: {}".format(params))

        commands =  ("cp /app/vnf/generator/generator.yml ./",
                     "snmp_generator generate --output-path=/etc/snmp_exporter/snmp.yml",
                     "touch /etc/snmp_exporter/generator.yml")
        for command in commands:
            return_code, stdout, stderr = await util_ee.local_async_exec(command)
            if return_code != 0:
                yield "ERROR", "return code {}: {}".format(return_code, stderr.decode())
                break
        else:
            yield "OK", stdout.decode()

    @staticmethod
    def _check_required_params(params, required_params):
        for required_param in required_params:
            if required_param not in params:
                raise VnfException("Missing required param: {}".format(required_param))
