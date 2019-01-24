# -*- coding: utf-8 -*-
# Copyright 2016 Dravetech AB. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

"""
Napalm driver for FortiGate FortiOS 6.x.

Read https://napalm.readthedocs.io for more information.
"""

# std libs

# Disable warnings about certificates.
import urllib3
urllib3.disable_warnings()

from requests.exceptions import (
    ConnectTimeout,
    ConnectionError,
    )

# third party libs
from fortiosapi import FortiOSAPI
#from fortiosapi.exceptions import NotLogged as NotLogged
# from fortiosapi.exceptions.NotLogged import NotLogged


# NAPALM Base
from napalm.base import NetworkDriver
from napalm.base.exceptions import (
    ConnectionException,
    SessionLockedException,
    MergeConfigException,
    ReplaceConfigException,
    CommandErrorException,
)


class FortiOS6Driver(NetworkDriver):
    """Napalm driver for FortiGate FortiOS 6.x."""

    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        """Constructor."""
        self.device = None
        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout

        if optional_args is None:
            optional_args = {}
        else:
            self.transport = optional_args.get("transport", "https")
            self.port = optional_args.get('port', 443)



        self.device = FortiOSAPI()

    def open(self):
        """Implement the NAPALM method open (mandatory)"""
        
        try:
            self.device.login(host = self.hostname,
                              username = self.username, 
                              password = self.password)
        
        except ConnectionError:
            print('Connection Error')


    def close(self):
        """Implement the NAPALM method close (mandatory)"""
        self.device.logout()

    def get_facts(self):
        facts = {}

        system_global = self.device.get('system', 'global')
        system_dns = self.device.get('system', 'dns')['results']        

        facts['hostname'] = system_global['results']['hostname']
        facts['fqdn'] = facts['hostname'] + '.' + system_dns['domain']
        facts['vendor'] = 'Fortinet'
        facts['model'] = None                                           # Unable to get from API
        facts['serial_number'] = system_global['serial']
        facts['os_version'] = system_global['version']
        facts['uptime'] = None                                          # Unable to get from API
        facts['interface_list'] = None

        return facts

    def is_alive(self):
        """Returns a flag with the state of the connection."""
        is_alive = False

        # Only consider device alive after logged in and successful response
        try:
            is_alive = self.device.get('system', 'status')['http_status']
        
        except NotLogged:
        # except fortiosapi.exceptions.NotLogged:
            is_alive = True
            print('cool')

        # except ConnectTimeout:
        #     pass
                
        except Exception as e:
            print(e.__class__)
            print(e.__class__ == NotLogged)
            print('Unknown Error')

        if is_alive:
            return {'is_alive': True}
        else:
            return {'is_alive': False}
