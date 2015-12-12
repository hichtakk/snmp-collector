#!/usr/bin/env python3

"""
Python asyncronouse SNMP collector.
"""

import asyncio
import json
import logging

from pysnmp.hlapi.asyncio import (SnmpEngine, getCmd, CommunityData,
                                  UdpTransportTarget, ContextData, ObjectType,
                                  ObjectIdentity)


CON_LIMIT = 1


class SnmpException(Exception):
    pass


@asyncio.coroutine
def run(host, ois, community="public", port=161):
    snmpEngine = SnmpEngine()
    result = []
    with (yield from asyncio.Semaphore(CON_LIMIT)):
        errorIndication, errorStatus, errorIndex, varBinds = yield from getCmd(
            snmpEngine,
            CommunityData(community, mpModel=1),
            UdpTransportTarget((host, port)),
            ContextData(),
            *[ObjectType(ObjectIdentity(o)) for o in ois]
        )
        if errorIndication:
            result.append({"status": "error", "indication": str(errorIndication)})
        elif errorStatus:
            print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex)-1][0] or '?'
                )
            )
        else:
            for varBind in varBinds:
                [oid, value] = [x for x in varBind]
                result.append({"host": host, "oid": str(oid), "type": value.__class__.__name__, "value": str(value) if value else None})
    snmpEngine.transportDispatcher.closeDispatcher()
    return result


def main():
    fd = open('./target.json')
    config = json.loads(fd.read())
    loop = asyncio.get_event_loop()
    tasks = []
    for host in config["targets"]:
        target_oid = [oid["oid"] for oid in host["oids"]]
        community = config["defaults"]["community"]
        task = run(host["address"], target_oid, community=community)
        tasks.append(task)
    results = loop.run_until_complete(asyncio.wait(tasks))
    for i in results[0]:
        for a in i.result():
            print(a)

if __name__ == '__main__':
    main()

