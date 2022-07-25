#!/usr/bin/env python

import asyncio
import websockets
import sys
import json

from pyais import decode

async def consumer_handler(websocket, path):

    async for message in websocket:
        print(message)

async def producer_handler(websocket, path):

    print("Producer running")

    for line in sys.stdin:
        d = json.loads(line)
        e = decode(*d["NMEA"]).asdict()

        if 'lat' in e.keys():
            v = {'mmsi' : d['mmsi'], 'lat' : e["lat"], 'lon' : e["lon"], 'power' : d['signalpower'], 'ppm' : d['ppm'], 'channel' : d['channel'] }

        await websocket.send(json.dumps(v))

async def handler(websocket, path):
    asyncio.ensure_future(consumer_handler(websocket, path))
    asyncio.ensure_future(producer_handler(websocket, path))

async def main():
    async with websockets.serve(handler, "", 8002):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
