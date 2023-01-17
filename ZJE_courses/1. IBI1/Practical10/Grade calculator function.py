# define a new function
def grade_calculator_function(name,code_grade,poster_grade,exam_grade):
    final_grade=0.4*code_grade + 0.3*poster_grade + 0.3*exam_grade
    return name,final_grade
# example
# The output is 'Sam 81.4'
name_example, grade_example = grade_calculator_function('Sam',70,80,98)
print(name_example,end=' ')
print(grade_example)

a=input('The student name is:')
b=input('The score of code is:')
c=input('The score of poster is:')
d=input('The score of exam is:')
name, grade =grade_calculator_function(a,float(b),float(c),float(d))
print(name,end=' ')
print(grade)


