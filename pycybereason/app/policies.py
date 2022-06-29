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
LOG = logging.getLogger(__name__)


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

    def compare(self, a: str = None, b: str = None) -> None:
        # recursive comparison
        def _compare(a, a_label, b, b_label, keys, res):
            has_nested_keys = False
            for k in a:
                # skip list
                if k in ['metadata', 'notes', 'description', 'name']:
                    continue

                if not isinstance(a[k], dict):  # we are in a leaf...
                    values_are_different = False
                    if isinstance(a[k], list):
                        values_are_different = (len(a[k]) != len(b[k]))
                    else:
                        values_are_different = (a[k] != b[k])
                    if values_are_different:
                        res['.'.join(keys+[k])] = {a_label: a[k], b_label: b[k]}
                else:  # go deep...
                    has_nested_keys = True
                    new_keys, new_res = _compare(a[k], a_label, b[k], b_label, keys+[k], res)

            if not has_nested_keys:
                return keys, res
            return new_keys, new_res

        # select policies
        def _select_policy(policies, prompt):
            print('')
            idx = None
            for k in policies:
                print(f'({k}) {policies[k]["name"]}')
            try:
                idx = int(input(f'[?] Select the {prompt} policy (0 - {len(policies)-1}): '))
            except Exception as e:
                idx = -1

            while idx not in policies:
                print('\n[!] Invalid policy! Retry...')
                for k in policies:
                    print(f'({k}) {policies[k]["name"]}')
                try:
                    idx = int(input(f'[?] Select the {prompt} policy (0 - {len(policies)-1}): '))
                except Exception as e:
                    idx = -1

            return policies[idx]['id']

        # get policies list (if needed)
        policies = {}
        idx = 0
        if (not a) or (not b):
            for p in self.api.policies.list():
                policies[idx] = p
                idx += 1

        # get id of A policy
        pol_a_id = None
        if not a:
            pol_a_id = _select_policy(policies, 'A')
        else:
            pol_a_id = a

        # get id of B policy
        pol_b_id = None
        if not b:
            pol_b_id = _select_policy(policies, 'B')
        else:
            pol_b_id = b

        # get configuration for policy a...
        pol_a = self.api.policies.dump(pol_a_id)
        if not pol_a:
            LOG.error(f'Unable to get configuration for policy: {pol_a_id}')
            return
        pol_a_label = pol_a['metadata']['name']

        # get configuration for policy b...
        pol_b = self.api.policies.dump(pol_b_id)
        if not pol_b:
            LOG.error(f'Unable to get configuration for policy: {pol_b_id}')
            return
        pol_b_label = pol_b['metadata']['name']

        # compare a and b policies
        keys, res = _compare(pol_a, pol_a_label,
                             pol_b, pol_b_label,
                             [], {})

        # print the result
        for k in res:
            print(f'----- {k} -----\n')
            print(f'>> {pol_a_label} <<\n\n{json.dumps(res[k][pol_a_label], indent=2, sort_keys=True)}\n')
            print(f'>> {pol_b_label} <<\n\n{json.dumps(res[k][pol_b_label], indent=2, sort_keys=True)}\n')
