from turtledemo.penrose import start
import scanner
import asyncio

import drive_to

async def find():
    start_position = -112000
    end_position = -48000
    counter = 10000

    currentX = start_position
    currentY = start_position

    # Starte den Scanner asynchron
    asyncio.create_task(scanner.scan(find_station))

    while True:
        await drive_to.set_target(currentX, currentY)

        if currentY == end_position or currentY :
            currentY = start_position
        else:
            currentY = end_position

        currentX += counter

        await asyncio.sleep(1)

def find_station(json_body):

    for obj in json_body:
        if obj.get('name') == 'Architect Colony':
            coordinates = obj.get('pos', {})
            x = coordinates.get('x', None)
            y = coordinates.get('y', None)
            if x is not None and y is not None:
                drive_to.set_target(x, y)
            else:
                print("Koordinaten für Architect Colony fehlen.")
