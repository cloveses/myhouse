class Person:

    def __init__(self, name, age, vocation, salary):
        self.name = name
        self.age = age
        self.vocation = vocation
        self.salary = salary

    def introduce(self):
        print('name:', self.name)
        print('age:', self.age)
        print('vocation:', self.vocation)

    def income(self):
        print("{}'s income: {}".format(self.name, self.salary))

    def tax(self):
        print("{}'s tax: {}".format(self.name, self.salary * 0.2))

    def __add__(self, person):
        print("total salary:", self.salary + person.salary)
        self.salary += person.salary
        return self

    def __call__(self):
        self.introduce()

if __name__ == '__main__':
    pa = Person('John', 32, 'teacher', 3460)
    pb = Person('Mary', 30, 'worker', 3580)
    pa.introduce()
    pa.income()
    pa.tax()
    pa()
    pc = pa + pb

