# Copyright 2022 Paolo Smiraglia <paolo.smiraglia@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import logging
from typing import Dict

from restfly.endpoint import APIEndpoint

# setup logging
LOG = logging.getLogger(__name__)


class Malops(APIEndpoint):
    _path = 'rest/detection'

    # list malops (inbox)
    def inbox(self, start_time: int, end_time: int, group_ids=None) -> Dict:
        payload = {'startTime': start_time, 'endTime': end_time}
        if group_ids:
            payload['groupIds'] = group_ids

        resp = {}
        try:
            resp = self._post('inbox', json=payload)
            resp = resp.json()
        except Exception as e:
            LOG.error(e)
        return resp

    # get details (details)
    def details(self, guid: str) -> Dict:
        payload = {'malopGuid': guid}
        resp = {}
        try:
            resp = self._post('details', json=payload).json()
        except Exception as e:
            LOG.error(e)
        return resp
