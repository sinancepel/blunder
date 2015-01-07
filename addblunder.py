""" Script to add a single blunder to the database. Useful when
    adding blunders from the command line.
"""
import peewee
from peewee import *
import os.path
import sys
db = 0
"""Connects to a database and returns db handle. 
   h: host, u: username, pwd: password, database: database name.
"""
def connect(h, u, pwd, database):
    global db
    db = MySQLDatabase(database, 
                       user=u,
                       passwd=pwd);
    
def init(config):
    exists = os.path.isfile(config)
    if not exists:
        print "Invalid config file"
        sys.exit(0)
    conf_file = open(config, "r")
    data = {}
    for line in conf_file:
        s = line.strip()
        kv_pair = s.split("=")
        if len(kv_pair) == 0:
            continue
        if not (len(kv_pair) == 2):
            print "Config file contains non key-value entry"
            continue
        data[kv_pair[0]] = kv_pair[1]
    connect(data["host"], data["user"], 
            data["passwd"], data["db"])

class Blunder(peewee.Model):
    type = peewee.CharField()
    description = peewee.TextField()
    class Meta:
        database = db

def run():
    if len(sys.argv) < 3: 
        print "Usage: ", sys.argv[0], "<blunder_type> <blunder_description> [show] [config_file]"
    if len(sys.argv) < 5:
        init("config")
    else:
        init(sys.argv[4])
    Blunder.create_table(True)
    blunder = Blunder(type=sys.argv[1], description=sys.argv[2])
    blunder.save()
    if len(sys.argv) > 3 and sys.argv[3] == "show":
        for blunder in Blunder.select():
            print blunder.type, blunder.description


run()
