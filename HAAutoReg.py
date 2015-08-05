#!/usr/bin/python
import sys
import pickle
import argparse
import os

class HAServer:
    def __init__(self, name="server", addr="0.0.0.0:2000", check="check"):
        self.name   = name
        self.addr   = addr
        self.check  = check

    def __str__(self):
        return "    server %s %s %s\n" % (self.name, self.addr, self.check)

class HAService:
    def __init__(self, name="service", laddr="0.0.0.0:2000", balance="roundrobin", mode="tcp"):
        self.name       = name
        self.laddr      = laddr
        self.balance    = balance
        self.mode       = mode
        self.servers    = {}

    def addServer(self, name, addr, check="check"):
        self.servers[name] = HAServer(name, addr, check)

    def delServer(self, name):
        self.servers.pop(name, None)

    def __str__(self):
        ret = """
listen %s %s
    balance %s
    mode %s
""" % (self.name, self.laddr, self.balance, self.mode)
        for k,i in self.servers.iteritems():
            ret += i.__str__()
        return ret

class HAConfig:
    def __init__(self, configfile="/etc/haproxy/haautoreg.conf"):
        self.configfile = configfile
        self.services = {}
        self.header ="""
global
        maxconn         32000
        ulimit-n        65536
        user            haproxy
        group           haproxy
        nbproc          2
        daemon

defaults
        log             global
        mode            tcp
        balance         roundrobin
        option          dontlognull
        retries         3
        contimeout      5000
        clitimeout      30000
        srvtimeout      30000
"""
    def writeConfig(self):
        with open(self.configfile, "wb") as target:
            pickle.dump(self, target)

    def addService(self, name, addr, balance, mode):
        self.services[name] = HAService(name, addr, balance, mode)
        self.writeConfig()

    def addServer(self, service, name, addr, check):
        try:
            self.services[service].addServer(name, addr, check)
            self.writeConfig()
        except KeyError:
            print "No service with that name."

    def delService(self, name):
        self.services.pop(name, None)
        self.writeConfig()

    def delServer(self, service, name):
        self.services[service].delServer(name)
        self.writeConfig()

    def __str__(self):
        ret = self.header
        for k,i in self.services.iteritems():
            ret += i.__str__()
        return ret

if __name__ == "__main__":
    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action")

    parser_a = subparsers.add_parser('addService', help='adds a service for HAProxy')
    parser_a.add_argument('--name', required=True, help="Name of the service to add")
    parser_a.add_argument('--addr', required=True, help="Address to listen for example: 0.0.0.0:2000")
    parser_a.add_argument('--balance', default="roundrobin", help="Balancing method, default='roundrobin'")
    parser_a.add_argument('--mode', default="tcp", help="mode, default='tcp'")

    parser_b = subparsers.add_parser('addServer', help='b help')
    parser_b.add_argument('--service', required=True, help='listen addr of service to add server, like 0.0.0.0:2000')
    parser_b.add_argument('--name', required=True, help='name of server')
    parser_b.add_argument('--addr', required=True, help='addr of server')
    parser_b.add_argument('--check', default='check', help='check type default: check')

    parser_c = subparsers.add_parser('delService', help="remove a service from HAProxy")
    parser_c.add_argument('--name', required=True, help="Name of the service to remove")

    parser_d = subparsers.add_parser('delServer', help="remove a server from a service")
    parser_d.add_argument('--service', required=True, help="Name of the service which from we remove a server")
    parser_d.add_argument('--name', required=True, help="Name of the server to remove")

    parser_p = subparsers.add_parser('print', help="prints generated HAProxy conf")
    x = parser.parse_args(sys.argv[1:])

    CONFIGFILE="./haautoreg.conf"
    if os.path.isfile(CONFIGFILE):
        # Read config
        with open(CONFIGFILE,"rb") as source:
            config = pickle.load(source)
    else:
        config = HAConfig(CONFIGFILE) #Remove this

    try:
        if x.action == "addService":
            config.addService(x.name, x.addr, x.balance, x.mode)
        elif x.action == "addServer":
            config.addServer(x.service, x.name, x.addr, x.check)
        elif x.action == "delService":
            config.delService(x.name)
        elif x.action == "delServer":
            config.delServer(x.service, x.name)
        elif x.action == "print":
            print config
    except KeyError:
        print "No match with that name (service or server)"
