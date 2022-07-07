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
import re

from restfly.endpoint import APIEndpoint

# setup logging
LOG = logging.getLogger(__name__)


def _parse_response(text: str, regex: str) -> str:
    value = None
    p = re.compile(regex, re.MULTILINE | re.IGNORECASE)
    try:
        m = p.search(text)
        groups = m.groupdict() if m else {}
        value = groups['value'] if 'value' in groups else None
    except Exception as e:
        LOG.warn(f'Something went wrong: {e}')
    return value


class Ping(APIEndpoint):
    _path = 'rest/ping'

    def _get_info(self, regex: str) -> str:
        value = None
        try:
            text = self._get().text
            value = _parse_response(text, regex)
        except Exception as e:
            LOG.warn(f'Something went wrong: {e}')
        return value

    def version(self):
        regex = r'^application\.version=(?P<value>.*)$'
        return self._get_info(regex)

    def uptime(self):
        regex = r'^uptime=(?P<value>.*)$'
        return self._get_info(regex)
