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

import argparse
import logging
import sys
from datetime import datetime as dt
from typing import Dict

# setup logging
LOG = logging.getLogger(__name__)


def _print(m: Dict, server: str, show_machines: bool) -> None:
    display_name = m.get('displayName')
    guid = m.get('guid')
    url = f'https://{server}.cybereason.net/#/detection-malop/{guid}'
    print(f'[MALOP] {display_name} (guid: {guid}, url: {url})')
    if show_machines:
        for s in m['machines']:
            print(f'[MALOP > MACHINE] {s["displayName"]}')


class MalopsSubcommand(object):

    def __init__(self, api, opts, *args, **kwargs):
        self.api = api
        self.opts = opts

    def inbox(self, args: argparse.Namespace) -> None:
        try:
            start_time = (dt.strptime(args.start_time,
                                      '%Y%m%dT%H%M%S').timestamp() * 1000)
            end_time = (dt.strptime(args.end_time,
                                    '%Y%m%dT%H%M%S').timestamp() * 1000)
        except Exception as e:
            LOG.error(e)
            sys.exit(1)

        group_ids = args.group_ids
        resp = self.api.malops.inbox(start_time, end_time, group_ids)
        for m in resp.get('malops'):
            if args.filter:
                if args.filter in m['displayName']:
                    _print(m, self.opts['server'], args.show_machines)
            else:
                _print(m, self.opts['server'], args.show_machines)
