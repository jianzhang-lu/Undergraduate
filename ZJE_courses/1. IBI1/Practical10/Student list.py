class Student:
    def __init__(self):
        pass
    def first_name(self,a):
        self.f_name = a
    def last_name(self,b):
        self.l_name = b
    def pro(self,c):
        if c=='BMS' or c=='BMI':
            self.programme=c
        else:
            raise ValueError('The programme must be BMI or BMS.')
    def information(self):
        print('The full name is', self.f_name, self.l_name, end='. ')
        print('The programme is', self.programme, end='.\n')

# the example
student1=Student()
student1.first_name('Michael')
student1.last_name('King')
student1.pro('BMI')
student1.information()

student2=Student()
result1=input('The first name is:')
result2=input('The last name is:')
result3=input('The programme is:')
student2.first_name(result1)
student2.last_name(result2)
student2.pro(result3)
student2.information()



