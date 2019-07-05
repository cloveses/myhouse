
def mycount(mystr):
    # 初始化字母和数字计数器为0
    alpha_num = 0
    digit_num = 0
    for c in mystr:
        if c.isdigit(): #判断为数字，则数字计数加1
            digit_num += 1
        elif c.isalpha(): #判断为字母，则字母计数加1
            alpha_num += 1
    print('alpha:{}, digit: {}'.format(alpha_num, digit_num))

class Person:
    # 定义构造函数
    def __init__(self,name,age,idCard):
        # 建立实例属性
        self.name = name
        self.age = age
        self.__IDCard = idCard

    #定义eat函数
    def eat(self):
        print(self.name, "在吃饭")

    def get_IDCard(self):
        # 输出并返回身份证号
        print(self.__IDCard)
        return self.__IDCard

#定义类
class BirthDate:
    # 定义构造函数
    def __init__(self, year, month, day):
        # 建立实例属性
        self.year = year
        self.month = month
        self.day = day

#定义继承Person类的Employee类
class Employee(Person):
    def __init__(self,name,age,idCard, post, salary, birthday):
        # 调用父类构造函数
        super().__init__(name,age,idCard)
        # 建立实例属性
        self.post = post
        self.salary = salary
        self.birthday = birthday

    def dowork(self,work):
        print('{}的职位是{}，薪金是{}，他擅长的工作是{}。'.format(self.name, self.post, self.salary, work))

# 实例化BirthDate
bd = BirthDate(2000,4,8)
# 实例化Employee
emp = Employee('张三', 19, '330627200004081236', '软件工程师', '12000',bd)
# 调用Employee类实例方法get_IDCard
idcard = emp.get_IDCard()
print(idcard)
# 调用Employee类实例方法dowork
emp.dowork('前端开发')


def sumn(str1):
    # 初始化记录计数的列表，前一个元素作为数字计数，后一个元素为字母计数
    list1 = [0,0]
    # 循环处理每个字符
    for i in str1:
        # 字符在0－9之间，即数字，就对数字计数加1
        if(i>='0' and i<='9' ):
            list1[0] = list1[0] + 1
        # 字符在a－z之间，即字母，就对字母计数加1
        if(i>='a'and i<='z'):
            list1[1] = list1[1] + 1
    #返回计数的列表        
    return list1


# if __name__ == '__main__':
#     mycount('ab22+c')
#     p = Person('aa', 12, '341324')
#     print(p.get_IDCard())