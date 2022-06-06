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

# setup logging
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(logging.Formatter('[%(name)s/%(levelname)5.5s] %(message)s'))
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
LOG.addHandler(sh)


class SensorsActions(object):
    def __init__(self, api):
        self.api = api

    def query(self, filters):
        f = None

        try:
            if filters.startswith('@'):
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
            LOG.warn(e)

        if not f:
            raise Exception(f'Unable to load filters from "{filters}"')

        sensors = self.api.sensors.query(f)
        for s in sensors:
            LOG.info(f'Sensor: {s["machineName"]}')
