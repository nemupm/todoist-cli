#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

    click.echo(date)

def main():
    command()

if __name__ == '__main__':
    main()
