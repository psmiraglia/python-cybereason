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

import json
import logging

# setup logging
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(logging.Formatter('[%(name)s][%(levelname)5.5s] %(message)s'))
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
LOG.addHandler(sh)


class PoliciesSubcommand(object):

    def __init__(self, api, *args, **kwargs):
        self.api = api

    def list(self) -> None:
        for p in self.api.policies.list():
            print(f'[*] {p["name"]} ({p["id"]})')

    def dump(self, policy_id: str, out_file: str = None) -> None:
        dump = self.api.policies.dump(policy_id)

        _out_file = f'policy-{policy_id}.json'
        if out_file:
            _out_file = out_file

        with open(_out_file, 'w') as fp:
            json.dump(dump, fp, sort_keys=True, indent=4)
            fp.close()

        LOG.info(f'Policy dump saved: {_out_file}')
