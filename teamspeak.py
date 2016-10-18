#!/usr/bin/python2
import os
import telnetlib
import re

import sys

serverids = [1]

host = os.getenv('teamspeak_host', '127.0.0.1')
port = os.getenv("teamspeak_port", 10011)

query_user = os.getenv('teamspeak_query_user', '')
query_user_password = os.getenv('teamspeak_query_user_password', '')

if __name__ == '__main__':
    if 'config' in sys.argv:
        print("""graph_title Teamspeak Users
graph_args --base 1000 -l 0
graph_vlabel Connected Teamspeak Users
graph_category Teamspeak
graph_info This graph shows the number of connected users on a Teamspeak3 server
TeamSpeak3.label users
TeamSpeak3.draw LINE2
TeamSpeak3.info The current number of users""")
        exit()

    ts = telnetlib.Telnet(host, int(port), timeout=3)
    ts.set_debuglevel(0)

    ts.read_until("for information on a specific command.\n\r", 5)

    for serverid in serverids:
        ts.write('use sid=%d\n\r' % serverid)
        ts.read_until('error id=0 msg=ok\n\r', 5)

        ts.write('login %s %s\n\r' % (query_user, query_user_password))
        ts.read_until('error id=0 msg=ok\n\r', 5)

        ts.write('serverinfo\n\r')

        serverinfo = ts.read_until('error id=0 msg=ok\n\r', 5)

        ts.close()

        res = re.findall('virtualserver_clientsonline=(\d+) .* virtualserver_queryclientsonline=(\d+)', serverinfo)

        # print('server%d %d' % (serverid, int(res[0][0]) - int(res[0][1])))
        print(u'TeamSpeak3.value %d' % round(int(res[0][0]) - int(res[0][1])))
