import time
import threading

def sub():
    for i in range(6):
        print('sleep..',threading.currentThread().getName())
        time.sleep(1)

def ma():
    print('Main thread...')
    time.sleep(1)

if __name__ == '__main__':
    ma()
    # t = threading.Thread(target=sub)
    # # t.setDaemon(True)
    # t.start()
    # t.join()
    # ta = threading.Thread(target=sub)
    # # ta.setDaemon(True)
    # ta.start()
    # ta.join()

    ts = []
    for i in range(2):
        ts.append(threading.Thread(target=sub))
    for t in ts:
        t.start()
    t.join()

    ma()
