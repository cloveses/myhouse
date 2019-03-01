from time import sleep
import signal

class Test:
    def __init__(self):
        self.stop = False

    def main(self):
        for i in range(300):
            print('aaa:',i)
            sleep(3)
            if self.stop:
                break

    def handler(self, s, f):
        self.stop = True

def main():
    t = Test()
    signal.signal(signal.SIGTSTP, t.handler)
    t.main()

if __name__ == '__main__':
    main()