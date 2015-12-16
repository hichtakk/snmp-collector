"""
asyncronouse SNMP collector.
"""

import asyncio

from pysnmp.hlapi.asyncio import (SnmpEngine, getCmd, CommunityData,
                                  UdpTransportTarget, ContextData, ObjectType,
                                  ObjectIdentity)


CONCURRENT_REQUEST_LIMIT = 5
sem = asyncio.Semaphore(CONCURRENT_REQUEST_LIMIT)


class SnmpException(Exception):
    pass


class SNMPCommand(object):

    def __init__(self):
        pass

    def get(self):
        pass

    def set(self):
        pass

    def walk(self):
        pass

    def bulkget(self):
        pass

    def bulkwalk(self):
        pass


class SNMPCollector(object):

    def __init__(self, config, semaphore=CONCURRENT_REQUEST_LIMIT):
        self._semaphore = asyncio.Semaphore(semaphore)
        self._config = config
    
    async def _collect(self, host, ois, community="public", port=161):
        snmpEngine = SnmpEngine()
        result = []
        with (await self._semaphore):
            errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
                snmpEngine,
                CommunityData(community, mpModel=1),
                UdpTransportTarget((host, port)),
                ContextData(),
                *[ObjectType(ObjectIdentity(o)) for o in ois]
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
                    result.append({"host": host, "oid": str(oid),
                                   "type": value.__class__.__name__,
                                   "value": str(value) if value else None})
        snmpEngine.transportDispatcher.closeDispatcher()
        return result

    def run(self):
        loop = asyncio.get_event_loop()
        tasks = []
        for host in self._config["targets"]:
            oids = [oid["oid"] for oid in host["oids"]]
            community = host["community"] if "community" in host else self._config["defaults"]["community"]
            tasks.append(self._collect(host["address"], oids, community=community))
        result = loop.run_until_complete(asyncio.wait(tasks))
        return result[0]


def main():
    import json
    import logging
    fd = open('./target.json')
    config = json.loads(fd.read())
    collector = SNMPCollector(config)
    results = collector.run()

    for task_result in results:
        print(type(task_result))
        for result in task_result.result():
            print(result)

    
if __name__ == '__main__':
    main()
