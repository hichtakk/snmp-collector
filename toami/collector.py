"""
asyncronouse SNMP collector.
"""

import asyncio
import time
import functools

from pysnmp.hlapi.asyncio import (SnmpEngine, getCmd, CommunityData,
                                  UdpTransportTarget, ContextData, ObjectType,
                                  ObjectIdentity)


CONCURRENT_REQUEST_LIMIT = 5


class SNMPCollector(object):

    def __init__(self, config, semaphore=CONCURRENT_REQUEST_LIMIT):
        self._semaphore = asyncio.Semaphore(semaphore)
        self._config = config
    
    async def _collect(self, hostname, address, oids, community="public", port=161):
        snmpEngine = SnmpEngine()
        result = []
        with (await self._semaphore):
            errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
                snmpEngine,
                CommunityData(community, mpModel=1),
                UdpTransportTarget((address, port)),
                ContextData(),
                *[ObjectType(ObjectIdentity(oid['oid'])) for oid in oids]
            )
            if errorIndication:
                result.append({"status": "error",
                               "indication": str(errorIndication)})
            elif errorStatus:
                print('%s at %s' % (
                        errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex)-1][0] or '?'
                    )
                )
            else:
                for varBind in varBinds:
                    [oid, value] = [x for x in varBind]
                    result.append({"host": hostname, "address": address, "oid": str(oid),
                                   "type": value.__class__.__name__,
                                   "value": str(value) if value else None,
                                   "time": int(time.time()),
                                   "label": [x for x in oids if x['oid'] == str(oid)].pop()['description']})
        snmpEngine.transportDispatcher.closeDispatcher()
        return result

    def run(self):
        loop = asyncio.get_event_loop()
        tasks = []
        for host in self._config["targets"]:
            community = host["community"] if "community" in host else self._config["defaults"]["community"]
            tasks.append(self._collect(host["name"], host["address"], host['oids'], community=community))
        result = loop.run_until_complete(asyncio.wait(tasks))
        ret = functools.reduce(lambda a,b: a+b, [x.result() for x in result[0]])
        return sorted(ret, key=lambda x:x['host'])


if __name__ == '__main__':
    pass
