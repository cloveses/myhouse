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
        
if __name__ == '__main__':
    white_cat = Cat('WhiteCat','white')
    red_cat = Cat('RedCat','red')
    blue_cat = Cat('BlueCat','blue')
    cats = [white_cat,red_cat,blue_cat]
    for cat in cats:
        print('Start...')
        cat.miaomiaobark()
        cat.eat()
        cat.jump()
        print()
