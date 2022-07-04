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

import csv
import json
import logging
import os
import sys
from typing import Dict, List

from tabulate import tabulate

# setup logging
LOG = logging.getLogger(__name__)


def _as_table(values, headers):
    tablefmt = 'pretty'
    colalign = []

    # build headers dictionary
    _headers = {}
    for k in headers:
        _headers[k] = k
        colalign.append('left')

    # filter values
    _values = []
    for v in values:
        _v = {}
        for k in headers:
            _v[k] = v[k]
        _values.append(_v)

    print(tabulate(_values, _headers, tablefmt, colalign=colalign))


def _as_csv(values: List[Dict], headers: List[str],
            out_file: str = None) -> None:
    # init CSV writer
    fp = None
    if out_file:
        fp = open(out_file, 'w')
        w = csv.writer(fp, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    else:
        w = csv.writer(sys.stdout, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

    # wite contents
    w.writerow(headers)
    for v in values:
        w.writerow([v[k] for k in headers])

    # close file pointer (if needed...)
    if fp:
        fp.close()


class SensorsSubcommand(object):

    def __init__(self, api, *args, **kwargs):
        self.api = api

    def query(self, cols: str, filters: str, os_type: str, out_file: str, out_form: str, status: str) -> None:  # noqa
        def _filters(filters: str) -> List[Dict]:
            f = []
            try:
                if not filters:
                    prompt = '[?] The query will return all the sensors. Should I proceed? [y/N] '  # noqa
                    a = input(prompt).lower()
                    while a not in ['y', 'n', '']:
                        a = input(prompt).lower()
                    if (a == 'n') or (not a):
                        sys.exit(0)
                elif filters.startswith('@'):
                    # load filters from file
                    ffile = filters[1:]
                    if not os.path.exists(ffile):
                        LOG.error(f'{ffile} does not exist')
                    else:
                        LOG.debug(f'Load filters from file ({ffile})')
                        with open(ffile, 'r') as fp:
                            f = json.load(fp)
                            fp.close()
                else:
                    # load filters from string
                    LOG.debug(f'Load filters from string ({filters})')
                    f = json.loads(filters)
            except Exception as e:
                LOG.error(f'Unable to load filters: {e}')
                sys.exit(1)
            return f

        sensors = []
        try:
            f = []
            if status or os_type:
                if status:
                    f.append({
                        'fieldName': 'status',
                        'operator': 'EqualsIgnoreCase',
                        'values': status
                    })
                if os_type:
                    f.append({
                        'fieldName': 'osType',
                        'operator': 'EqualsIgnoreCase',
                        'values': os_type
                    })
            else:
                f = _filters(filters)
            sensors = self.api.sensors.query(f)
            if out_form == 'CSV':
                _as_csv(sensors, cols, out_file)
                if out_file:
                    print(f'(*) Query results saved on {out_file}')
            else:
                _as_table(sensors, cols)
                print(f'(*) Number of sensors: {len(sensors)}')
        except Exception as e:
            LOG.error(e)

    def logs(self, sensors: List[str]) -> None:
        for s in sensors:
            print(f'(*) Getting log for sensor: {s}')
