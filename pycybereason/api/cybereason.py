# Copyright 2022 Paolo Smiraglia <paolo.smiraglia@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging

from restfly.session import APISession

from pycybereason.api.policies import Policies
from pycybereason.api.sensors import Sensors

# setup logging
LOG = logging.getLogger(__name__)


class Cybereason(APISession):
    _ssl_verify = True

    def __init__(self, server, **kwargs):
        self._url = f'https://{server}.cybereason.net:443'
        super(Cybereason, self).__init__(**kwargs)

    def _authenticate(self, **kwargs):
        username = kwargs.pop('username', None)
        password = kwargs.pop('password', None)
        if username and password:
            self.post('login.html', data={
                'username': username,
                'password': password
            })
        else:
            raise Exception('Missing credentials')

    @property
    def sensors(self):
        return Sensors(self)

    @property
    def policies(self):
        return Policies(self)
