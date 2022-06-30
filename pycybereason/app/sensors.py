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
import os
import sys
from typing import Dict, List

# setup logging
LOG = logging.getLogger(__name__)


class SensorsSubcommand(object):

    def __init__(self, api, *args, **kwargs):
        self.api = api

    def query(self, filters: str) -> None:
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
            f = _filters(filters)
            sensors = self.api.sensors.query(f)
            for s in sensors:
                print(f'(*) Sensor: {s["machineName"]} ({s["sensorId"]})')
            print(f'(*) Number of sensors: {len(sensors)}')
        except Exception as e:
            LOG.error(e)

    def logs(self, sensors: List[str]) -> None:
        for s in sensors:
            print(f'(*) Getting log for sensor: {s}')