#!/usr/bin/env python3

from stockDbSync.djangoORM.djangoorm import ORMConfigBox

import os

def config_db():
    orm_conf = ORMConfigBox()
    orm_conf.set_apps(('stockDbSync.stockmodels',))
    try:
        orm_conf.name = DB_USER
    except:
        orm_conf.name = 'testing'
    try:
        orm_conf.user = DB_USER
    except:
        orm_conf.user = 'testing'
    try:
        orm_conf.password = DB_PASS
    except:
        orm_conf.password = 'testing'
    orm_conf.host = 'localhost'
    orm_conf.engine = 'postgres'
    orm_conf.init_db_settings()
    orm_conf.sync_db_schema()
    global fetch
    from stockDbSync.acquisition import fetch as fetch

def sync():
    fetch.update()

def execfile(fname):
    with open(fname) as f:
        code = compile(f.read(), fname, 'exec')
        exec(code)

if __name__ == '__main__':
    execfile(os.path.join(os.environ['HOME'], '.config', 'stockdb', 'dbsettings.py'))
    config_db()
    sync()
