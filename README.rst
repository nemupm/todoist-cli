Todoist CLI
=====================================

Unofficial CLI to use Todoist with Google Calendar

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

Usage
---------------

schedule
""""""""""
::

    $ todoist-cli schedule --help
    Usage: todoist-cli schedule [OPTIONS]

    Options:
      --date TEXT  Specify date as format YYYYMMDD
      --help       Show this message and exit.

