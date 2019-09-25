import unittest

class MyQueue:

    def __init__(self, data=None):
        self.data =  data
        self.pnext = None
        self.__count = 0

    def Enqueue(self, data):
        if not self.pnext:
            self.pnext = MyQueue(data)
        else:
            np = self.pnext
            for i in range(self.__count - 1):
                np = np.pnext
            np.pnext = MyQueue(data)
        self.__count += 1

    def PrintQueue(self):
        pn = self.pnext
        if not pn:
            print('Empty!')
        else:
            while pn:
                print(pn.data, end=' ')
                pn = pn.pnext
            print()

    def Dequeue(self):
        if not self.pnext:
            return None
        first = self.pnext
        second = first.pnext
        self.pnext = second
        self.__count -= 1
        return first.data

    def Count(self):
        return self.__count

    def Contains(self, data):
        if not self.pnext:
            print('Not find!')
            return False
        else:
            pn = self.pnext
            while True:
                if not pn:
                    return False
                else:
                    if pn.data == data:
                        return True
                    pn = pn.pnext

class TestMyQueue(unittest.TestCase):
    def test_fun(self):
        q = MyQueue()
        # q.PrintQueue()
        for i in range(10):
            q.Enqueue(i)
        self.assertEqual(q.Count(),10)
        for i in range(3):
            self.assertEqual(q.Dequeue(), i)
            self.assertEqual(q.Count(), 10-i-1)
        self.assertTrue(q.Contains(4))
        self.assertTrue(q.Contains(9))
        self.assertFalse(q.Contains(100))


if __name__ == '__main__':
    unittest.main()
        # q.Enqueue(1)
        # q.PrintQueue()
        # q.Enqueue(2)
        # q.PrintQueue()
        # for i in range(3,8):
        #     q.Enqueue(i)
        # q.PrintQueue()
        # print(q.Count())
        # for i in range(6,9):
        #     print(i, q.Contains(i))