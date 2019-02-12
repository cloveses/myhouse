from multiprocessing import Pool, Process
import asyncio, time

async def dostha(x):
    asyncio.sleep(5)
    time.sleep(1)
    print(x)

async def dosth():
    tasks = []
    print('x')
    for i in range(8):
        tasks.append(asyncio.ensure_future(dostha(i)))
    await asyncio.wait(tasks)
    return 7

def main(y):
    print(y)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dosth())

if __name__ == '__main__':
    ps = []
    for i in range(3):
        ps.append(Process(target=main, args=(90,)))
    for p in ps:
        p.start()
    p.join()