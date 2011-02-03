#! /usr/bin/python
from twisted.enterprise import adbapi
from twisted.internet import reactor

dbpool = adbapi.ConnectionPool("psycopg2", cp_min=3, cp_max=10, user='postgres', host='localhost', database='postgres', cp_noisy=True, cp_reconnect=True)

def get(x):
    return dbpool.runQuery("SELECT now()::text, " + str(x))

def printResult(l):
    if l:
        for item in l:
            print item
    else: 
        print "No such number"

def printError(failure):
	import sys
	sys.stderr.write(str(failure))

for x in range(100):
    get(x).addCallback(printResult)
    get(x).addErrback(printError)

reactor.suggestThreadPoolSize(10)
reactor.callLater(2, reactor.stop)
reactor.run()
