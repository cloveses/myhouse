class Animal:
    def __init__(self,name,zhonglei):
        self.name = name
        self.zhonglei = zhonglei

    def eat(self):
        print('The',self.zhonglei,self.name,'is eating.')

    def jump(self):
        print('The',self.zhonglei,self.name,'is jumping.')

class Cat(Animal):
    def __init__(self,name,zhonglei):
        super().__init__(name,zhonglei)

    def miaomiaobark(self):
        print('The',self.zhonglei,self.name,'Miao Miao!')

class Dog(Animal):
    def __init__(self,name,zhonglei):
        super().__init__(name,zhonglei)

    def wangwangbark(self):
        print('The',self.zhonglei,self.name,'Wang Wang!')


if __name__ == '__main__':
    black_cat = Cat('BlackCat','black')
    yellow_dog = Dog('YellowDog','yellow')
    print('Cat start...')
    black_cat.eat()
    black_cat.jump()
    black_cat.miaomiaobark()
    print()
    print('Dog start...')
    yellow_dog.eat()
    yellow_dog.jump()
    yellow_dog.wangwangbark()
