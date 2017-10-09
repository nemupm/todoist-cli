Todoist CLI
=====================================

Unofficial CLI to automatically schedule today Todoist items.

Example
---------------
::
    $ todoist-cli schedule --now

Before
""""""""""
![before](https://user-images.githubusercontent.com/8213881/31333343-93e7b136-ad24-11e7-9968-4ab844375501.png)

After
""""""""""
![after](https://user-images.githubusercontent.com/8213881/31333389-df7578e0-ad24-11e7-806d-e0fd0aa1bc81.png)

* run at 19:00.
* default item duration is 60 min.

Installation
---------------
::

    $ python setup.py sdist
    $ pip uninstall todoist-cli # if already installed
    $ pip install dist/todoist-cli-0.0.1.tar.gz

Setting
---------------
::

    $ cat $HOME/.todoist_cli/config.ini
    [todoist]
    token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    [calendar]
    key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    [settings]
    day_start=09:30
    default_duration_minutes=60

Usage
---------------

schedule
""""""""""
::

    $ todoist-cli schedule --help
    Usage: todoist-cli schedule [OPTIONS]

    Options:
      --date TEXT  (not implemented) Specify date as format YYYYMMDD
      --now        use the current time as day start time
      --help       Show this message and exit.

