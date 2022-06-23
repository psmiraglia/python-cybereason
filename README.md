# Cybereason

Command line interface for Cybereason.

## Install

~~~
$ virtualenv -p python3 .venv
$ . .venv/bin/activate
$ pip install .
~~~

## Get help

~~~
$ crcli --help

                   _____      _
                  / ____|    | |
      _ __  _   _| |    _   _| |__   ___ _ __ ___  __ _ ___  ___  _ __
     | '_ \| | | | |   | | | | '_ \ / _ \ '__/ _ \/ _` / __|/ _ \| '_ \
     | |_) | |_| | |___| |_| | |_) |  __/ | |  __/ (_| \__ \ (_) | | | |
     | .__/ \__, |\_____\__, |_.__/ \___|_|  \___|\__,_|___/\___/|_| |_|
     | |     __/ |       __/ |
     |_|    |___/       |___/  v0.1a0

 
usage: crcli [-h] [-s SERVER] [-u USERNAME] [-p PASSWORD] [-c CONF]
             {sensors,policies} ...

positional arguments:
  {sensors,policies}

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
  -u USERNAME, --username USERNAME
  -p PASSWORD, --password PASSWORD
  -c CONF, --conf CONF
~~~

## Examples

List policies

~~~
$ CRCLI_LOG_LEVEL=INFO crcli -c conf.json policies list

                   _____      _
                  / ____|    | |
      _ __  _   _| |    _   _| |__   ___ _ __ ___  __ _ ___  ___  _ __
     | '_ \| | | | |   | | | | '_ \ / _ \ '__/ _ \/ _` / __|/ _ \| '_ \
     | |_) | |_| | |___| |_| | |_) |  __/ | |  __/ (_| \__ \ (_) | | | |
     | .__/ \__, |\_____\__, |_.__/ \___|_|  \___|\__,_|___/\___/|_| |_|
     | |     __/ |       __/ |
     |_|    |___/       |___/  v0.1a0

 
[*] Servers (6abe26b0-4708-41f0-aa89-4ecb5a5be964)
[*] Clients (667295f9-9cca-46fc-aba2-40dad13ee0ec)
[*] Critical Servers (f5f5ed9e-d8a3-4621-b761-268152e3560b)
~~~

Dump policy configuration

~~~
$ CRCLI_LOG_LEVEL=INFO crcli -c conf.json policies dump --policy-id f5f5ed9e-d8a3-4621-b761-268152e3560b

                   _____      _
                  / ____|    | |
      _ __  _   _| |    _   _| |__   ___ _ __ ___  __ _ ___  ___  _ __
     | '_ \| | | | |   | | | | '_ \ / _ \ '__/ _ \/ _` / __|/ _ \| '_ \
     | |_) | |_| | |___| |_| | |_) |  __/ | |  __/ (_| \__ \ (_) | | | |
     | .__/ \__, |\_____\__, |_.__/ \___|_|  \___|\__,_|___/\___/|_| |_|
     | |     __/ |       __/ |
     |_|    |___/       |___/  v0.1a0

 
INFO: pycybereason.app.policies: Policy dump saved: policy-f5f5ed9e-d8a3-4621-b761-268152e3560b.json
~~~

Query sensors by loading filters from file

~~~
$ CRCLI_LOG_LEVEL=INFO crcli -c conf.json sensors query --filters @filters.json

                   _____      _
                  / ____|    | |
      _ __  _   _| |    _   _| |__   ___ _ __ ___  __ _ ___  ___  _ __
     | '_ \| | | | |   | | | | '_ \ / _ \ '__/ _ \/ _` / __|/ _ \| '_ \
     | |_) | |_| | |___| |_| | |_) |  __/ | |  __/ (_| \__ \ (_) | | | |
     | .__/ \__, |\_____\__, |_.__/ \___|_|  \___|\__,_|___/\___/|_| |_|
     | |     __/ |       __/ |
     |_|    |___/       |___/  v0.1a0


INFO: pycybereason.actions.sensors: Sensor: sql03
INFO: pycybereason.actions.sensors: Sensor: sql12
~~~
