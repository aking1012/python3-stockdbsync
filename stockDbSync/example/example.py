#!/usr/bin/env python3

from stockDbSync import stockdbsync
import os

if __name__ == '__main__':
    stockdbsync.execfile(os.path.join(os.environ['HOME'], '.config', 'stockdb', 'dbsettings.py'))
    stockdbsync.config_db()
    stockdbsync.sync()
