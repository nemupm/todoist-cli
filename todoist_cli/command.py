#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.dirname(os.path.join(os.getcwd(), os.pardir)))
from todoist_cli.client import Client
import click
from datetime import datetime

@click.group()
def command():
    pass

@command.command()
@click.option('--date', help='Specify date as format YYYYMMDD')
def schedule(date):
    def validate(date_text):
        try:
            datetime.strptime(date_text, "%Y%m%d")
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYYMMDD")

    if date:
        validate(date)
    else:
        date = datetime.today().strftime("%Y%m%d")

    client = Client('schedule', {'date': date})
    client.run()

def main():
    command()

if __name__ == '__main__':
    main()
