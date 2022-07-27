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
$ crcli -c conf.json sensors query --filters @filters.json

                   _____      _
                  / ____|    | |
      _ __  _   _| |    _   _| |__   ___ _ __ ___  __ _ ___  ___  _ __
     | '_ \| | | | |   | | | | '_ \ / _ \ '__/ _ \/ _` / __|/ _ \| '_ \
     | |_) | |_| | |___| |_| | |_) |  __/ | |  __/ (_| \__ \ (_) | | | |
     | .__/ \__, |\_____\__, |_.__/ \___|_|  \___|\__,_|___/\___/|_| |_|
     | |     __/ |       __/ |
     |_|    |___/       |___/  v0.1a0


+---------------+
| machineName   |
+---------------+
| sql03         |
| sql12         |
+---------------+
~~~

Query sensors by loading filters from file and by specifying details to be shown

~~~
$ crcli -c conf.json sensors query --filters @filters.json --cols machineName osType status

                   _____      _
                  / ____|    | |
      _ __  _   _| |    _   _| |__   ___ _ __ ___  __ _ ___  ___  _ __
     | '_ \| | | | |   | | | | '_ \ / _ \ '__/ _ \/ _` / __|/ _ \| '_ \
     | |_) | |_| | |___| |_| | |_) |  __/ | |  __/ (_| \__ \ (_) | | | |
     | .__/ \__, |\_____\__, |_.__/ \___|_|  \___|\__,_|___/\___/|_| |_|
     | |     __/ |       __/ |
     |_|    |___/       |___/  v0.1a0

+---------------+---------+--------+
| machineName   | osType  | status |
+---------------+---------+--------+
| sql03         | WINDOWS | Stale  |
| sql12         | WINDOWS | Stale  |
+---------------+---------+--------+
~~~

Compare policies (interactive)

~~~
$ crcli -c conf.json policies compare

                   _____      _
                  / ____|    | |
      _ __  _   _| |    _   _| |__   ___ _ __ ___  __ _ ___  ___  _ __
     | '_ \| | | | |   | | | | '_ \ / _ \ '__/ _ \/ _` / __|/ _ \| '_ \
     | |_) | |_| | |___| |_| | |_) |  __/ | |  __/ (_| \__ \ (_) | | | |
     | .__/ \__, |\_____\__, |_.__/ \___|_|  \___|\__,_|___/\___/|_| |_|
     | |     __/ |       __/ |
     |_|    |___/       |___/  v0.1a0

 

(0) Policy Alpha
(1) Policy Beta
(2) Policy Gamma
[?] Select the A policy (0 - 2): 2

(0) Policy Alpha
(1) Policy Beta
(2) Policy Gamma
[?] Select the B policy (0 - 2): 0

Comparison saved to compare-9034336c-0a4e-4461-b93b-f2153a55ed96--1e798691-4eb7-4f2c-98e8-a5d70c63d79b.txt
~~~

Compare policies (with options)

~~~
$ crcli -c conf.json policies compare -a 9034336c-0a4e-4461-b93b-f2153a55ed96 -b 1e798691-4eb7-4f2c-98e8-a5d70c63d79b -o mycompare.txt

                   _____      _
                  / ____|    | |
      _ __  _   _| |    _   _| |__   ___ _ __ ___  __ _ ___  ___  _ __
     | '_ \| | | | |   | | | | '_ \ / _ \ '__/ _ \/ _` / __|/ _ \| '_ \
     | |_) | |_| | |___| |_| | |_) |  __/ | |  __/ (_| \__ \ (_) | | | |
     | .__/ \__, |\_____\__, |_.__/ \___|_|  \___|\__,_|___/\___/|_| |_|
     | |     __/ |       __/ |
     |_|    |___/       |___/  v0.1a0

 
Comparison saved to mycompare.txt
~~~

Upgrade sensors

~~~
$ crcli -c conf.json sensors upgrade --filters @filters.json 

                   _____      _
                  / ____|    | |
      _ __  _   _| |    _   _| |__   ___ _ __ ___  __ _ ___  ___  _ __
     | '_ \| | | | |   | | | | '_ \ / _ \ '__/ _ \/ _` / __|/ _ \| '_ \
     | |_) | |_| | |___| |_| | |_) |  __/ | |  __/ (_| \__ \ (_) | | | |
     | .__/ \__, |\_____\__, |_.__/ \___|_|  \___|\__,_|___/\___/|_| |_|
     | |     __/ |       __/ |
     |_|    |___/       |___/  v0.1a0

 
[*] Scheduling upgrate for
[-]   sql03 (version: 20.2.222.0, id: 112233445566778899112233:PYLUMCLIENT_ANTANI_SQL03_0050568611AA)
[-]   sql12 (version: 20.1.343.0, id: 112233445566778899112233:PYLUMCLIENT_ANTANI_SQL12_00505686BB22)
Should I proceed? [y/n]
~~~

Show malops in a time range

~~~
$ crcli -c conf.json malops inbox --start-time '20220722T000000' --end-time '20220722T235959'

                   _____      _
                  / ____|    | |
      _ __  _   _| |    _   _| |__   ___ _ __ ___  __ _ ___  ___  _ __
     | '_ \| | | | |   | | | | '_ \ / _ \ '__/ _ \/ _` / __|/ _ \| '_ \
     | |_) | |_| | |___| |_| | |_) |  __/ | |  __/ (_| \__ \ (_) | | | |
     | .__/ \__, |\_____\__, |_.__/ \___|_|  \___|\__,_|___/\___/|_| |_|
     | |     __/ |       __/ |
     |_|    |___/       |___/  v0.1a0

 
[MALOP] system.componentmodel.dataannotations.ni.dll (guid: jVLbH23o4vyybRY7, url: https://antani.cybereason.net/#/detection-malop/jVLbH23o4vyybRY7)
[MALOP] windowsbase.ni.dll (guid: A0Qzt3G1yGIkYci3, url: https://antani.cybereason.net/#/detection-malop/A0Qzt3G1yGIkYci3)
~~~

Show malops in a time range, with details of affected machines

~~~
$ crcli -c conf.json malops inbox --start-time '20220722T000000' --end-time '20220722T235959' --show-machines

                   _____      _
                  / ____|    | |
      _ __  _   _| |    _   _| |__   ___ _ __ ___  __ _ ___  ___  _ __
     | '_ \| | | | |   | | | | '_ \ / _ \ '__/ _ \/ _` / __|/ _ \| '_ \
     | |_) | |_| | |___| |_| | |_) |  __/ | |  __/ (_| \__ \ (_) | | | |
     | .__/ \__, |\_____\__, |_.__/ \___|_|  \___|\__,_|___/\___/|_| |_|
     | |     __/ |       __/ |
     |_|    |___/       |___/  v0.1a0

 
[MALOP] system.componentmodel.dataannotations.ni.dll (guid: jVLbH23o4vyybRY7, url: https://antani.cybereason.net/#/detection-malop/jVLbH23o4vyybRY7)
[MALOP > MACHINE] sql03
[MALOP > MACHINE] sql12
[MALOP] windowsbase.ni.dll (guid: A0Qzt3G1yGIkYci3, url: https://antani.cybereason.net/#/detection-malop/A0Qzt3G1yGIkYci3)
[MALOP > MACHINE] sql03
[MALOP > MACHINE] sql12
~~~

Show malops in a time range, with details of affected machines and by filtering on the malop title

~~~
$ crcli -c conf.json malops inbox --start-time '20220722T000000' --end-time '20220722T235959' --show-machines --filter 'dataannotations.ni.dll'

                   _____      _
                  / ____|    | |
      _ __  _   _| |    _   _| |__   ___ _ __ ___  __ _ ___  ___  _ __
     | '_ \| | | | |   | | | | '_ \ / _ \ '__/ _ \/ _` / __|/ _ \| '_ \
     | |_) | |_| | |___| |_| | |_) |  __/ | |  __/ (_| \__ \ (_) | | | |
     | .__/ \__, |\_____\__, |_.__/ \___|_|  \___|\__,_|___/\___/|_| |_|
     | |     __/ |       __/ |
     |_|    |___/       |___/  v0.1a0

 
[MALOP] system.componentmodel.dataannotations.ni.dll (guid: jVLbH23o4vyybRY7, url: https://antani.cybereason.net/#/detection-malop/jVLbH23o4vyybRY7)
[MALOP > MACHINE] sql03
[MALOP > MACHINE] sql12
~~~
