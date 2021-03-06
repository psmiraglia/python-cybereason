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
import csv
import datetime
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


class SensorsSubcommand(object):

    def __init__(self, api, *args, **kwargs):
        self.api = api

    def query(self, cols: str, filters: str, os_type: str, out_file: str, out_form: str, status: str) -> None:  # noqa
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

    def upgrade(self, args: argparse.Namespace) -> None:
        limit = int(args.limit)
        filters = args.filters
        assume_yes = args.assume_yes
        out_file = args.out_file
        batch_file = args.batch_file

        # get batch info
        if batch_file:
            batch_data = {}
            with open(batch_file, 'r') as fp:
                batch_data = json.load(fp)
                fp.close()

            batch_id = batch_data.get('batchId')
            if not batch_id:
                print(f'[!] Invalid batch file: {batch_file}')
                sys.exit(1)
            resp = self.api.sensors.batch(batch_id)

            sensors = resp.get('sensors')
            if not sensors:
                print('[!] Unexpected response: sensors key is missing')
                sys.exit(1)

            print('[*] Outdated sensors')
            for s in [_s for _s in sensors if _s['outdated']]:
                name = s.get('machineName')
                v = s.get('version')
                sid = s.get('sensorId')
                print(f'[-] {name} (version: {v}, id: {sid})')

            print('[*] Updated sensors')
            for s in [_s for _s in sensors if not _s['outdated']]:
                name = s.get('machineName')
                v = s.get('version')
                sid = s.get('sensorId')
                print(f'[-] {name} (version: {v}, id: {sid})')
        else:
            # get list of sensors
            f = _filters(filters)
            sensors = self.api.sensors.query(f)
            if len(sensors) > limit:
                sensors = sensors[0:limit]

            # ask for confirmation
            print('[*] Scheduling upgrate for')
            for s in sensors:
                name = s.get('machineName')
                v = s.get('version')
                sid = s.get('sensorId')
                print(f'[-]   {name} (version: {v}, id: {sid})')

            choice = 'y'
            if not assume_yes:
                prompt = 'Should I proceed? [y/n] '
                choice = input(prompt)
                while choice not in ['y', 'n', 'Y', 'N']:
                    choice = input(prompt)

            # schedule th eupgrade (if confirmed)
            if choice.lower() == 'y':
                sensors_ids = [s['sensorId'] for s in sensors]
                resp = self.api.sensors.upgrade(sensors_ids=sensors_ids)

                # save references
                now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                batch_id = resp['batchId'] if 'batchId' in resp else 'None'
                action_type = resp['actionType'] if 'actionType' in resp else 'None'  # noqa
                print(f'[*] New batch: {action_type} ({batch_id})')

                _out_file = f'batch-{action_type}-{now}.json'
                if out_file:
                    _out_file = out_file
                with open(_out_file, 'w') as fp:
                    json.dump(resp, fp)
                    fp.close()
                print(f'[*] Job details saved on {_out_file}')
            else:
                print('[*] Upgrade aborted')
