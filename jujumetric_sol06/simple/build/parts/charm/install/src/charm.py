#!/usr/bin/env python3
##
# Copyright 2020 Canonical Ltd.
# All rights reserved.
#
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

import sys
import subprocess

sys.path.append("lib")
import logging

from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus

logger = logging.getLogger(__name__)

def get_metric(cmd):
    out = subprocess.check_output(cmd, shell=True)
    out = out.decode("utf-8").strip()
    return float(out)

class MyNativeCharm(CharmBase):

    def __init__(self, *args):
        super().__init__(*args)

        # Listen to charm events

        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.start, self._on_start)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.update_status, self._on_update_status)
        self.framework.observe(self.on.collect_metrics, self.on_collect_metrics)


        # Listen to the touch action event
        self.framework.observe(self.on.touch_action, self.on_touch_action)


    
    def _on_config_changed(self, _):
        self.unit.status = ActiveStatus()

    def _on_update_status(self, _):
        self.unit.status = ActiveStatus()

    def _on_install(self, event):
        """Called when the charm is being installed"""
        self.model.unit.status = ActiveStatus()

    def _on_start(self, event):
        """Called when the charm is being started"""
        self.model.unit.status = ActiveStatus()

    def on_touch_action(self, event):
        """Touch a file."""

        filename = event.params["filename"]
        try:
            subprocess.run(["touch", filename], check=True)
            event.set_results({"created": True, "filename": filename})
        except subprocess.CalledProcessError as e:
            event.fail("Action failed: {}".format(e))
        self.model.unit.status = ActiveStatus()

    def on_collect_metrics(self, event):
        mem_free = get_metric("free | grep Mem | awk '{print 100*$3/$2}'")
        cpu_util = get_metric("top -b -n2 | grep \"Cpu(s)\"|tail -n 1 | awk '{print $2 + $4}'")

        logger.debug(f"Free memory: {mem_free}")
        logger.debug(f"Cpu utilization: {cpu_util}")

        event.add_metrics({"mem_free": int(mem_free), "cpu_util": int(cpu_util)})




if __name__ == "__main__":
    main(MyNativeCharm)

