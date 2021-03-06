#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.dirname(os.path.join(os.getcwd(), os.pardir)))
from todoist_cli.client import Client
from datetime import datetime
import click

@click.group()
def command():
    pass

@command.command()
@click.option('--date', help='(not implemented) Specify date as format YYYYMMDD')
@click.option('--now', is_flag=True, help='use the current time as day start time')
def schedule(date, now):
    def validate(date_text):
        try:
            datetime.strptime(date_text, "%Y%m%d")
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYYMMDD")

    if date:
        validate(date)
    else:
        date = datetime.today().strftime("%Y%m%d")

    client = Client('schedule', {
        'date': date,
        'now': True if now else False
    })
    client.run()

@command.command()
def reset():
    client = Client('reset', {})
    client.run()

def main():
    command()

if __name__ == '__main__':
    main()
